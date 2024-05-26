# Released under the MIT License. See LICENSE for details.
#
"""Parser."""

from __future__ import annotations
from typing import Optional, Union

from dataclasses import dataclass

from io import BytesIO
from pynbs import Layer, Note, Parser, Instrument

import json

TEMPO = (
    20.0, 10.0, 6.67, 5.0, 4.0,
    3.33, 2.86, 2.5, 2.22, 2.0,
    1.82, 1.67, 1.54, 1.43, 1.33,
    1.25, 1.18, 1.11, 1.05, 1.0,
    0.95, 0.91, 0.87, 0.83, 0.8,
    0.77, 0.74, 0.71, 0.69, 0.67,
    0.65, 0.62, 0.61, 0.59, 0.57,
    0.56, 0.54, 0.53, 0.51, 0.5,)

BASE_INSTRUMENTS = (
    'block.note_block.harp',
    'block.note_block.bass',
    'block.note_block.basedrum',
    'block.note_block.snare',
    'block.note_block.hat',
    'block.note_block.guitar',
    'block.note_block.flute',
    'block.note_block.bell',
    'block.note_block.chime',
    'block.note_block.xylophone',
    'block.note_block.iron_xylophone',
    'block.note_block.cow_bell',
    'block.note_block.didgeridoo',
    'block.note_block.bit',
    'block.note_block.banjo',
    'block.note_block.pling',)


@dataclass
class Header:
    author: str
    name: str
    tempo: float
    length: int
    tick_delay: int
    duration: int
    duration_string: str 
    loop: bool
    loop_count: int
    loop_start: int
    
    old_author: str
    old_original: str
    old_name: str
    old_tempo: float
    old_loop: bool
    old_loop_count: int
    old_loop_start: int


def get_duration_string(seconds) -> str:
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return '{}:{:02d}'.format(minutes, remaining_seconds)

# def get_metadata(nbs_file: BytesIO) -> Union[
#     tuple[Header, list[Note], list[Layer],], str]:
def get_nbs_data(nbs_file: BytesIO) -> Optional[tuple[Header, 
                                                      list[Note], 
                                                      list[Layer],],]:
                                                    #   Optional[
                                                    #       list[Instrument],] 
    """
    TODO
    """
    try:
        nbs_data = Parser(nbs_file).read_file()
    except Exception:
        return None
    
    old = nbs_data.header

    seconds = (TEMPO.index(old.tempo)+1)*old.song_length//20 if (
        old.tempo in TEMPO) else 0

    header = Header(
        author=old.song_author,
        name=old.song_name,
        tempo=old.tempo,
        length=old.song_length,
        tick_delay=TEMPO.index(old.tempo)+1 if (old.tempo in TEMPO) else 0,
        duration=seconds,
        duration_string=get_duration_string(seconds),
        loop=False,
        loop_count=old.max_loop_count,
        loop_start=old.loop_start,

        old_author=old.song_author,
        old_original=old.original_author,
        old_name=old.song_name,
        old_tempo=old.tempo,
        old_loop=old.loop,
        old_loop_count=old.max_loop_count,
        old_loop_start=old.loop_start,)

    return header, nbs_data.notes, nbs_data.layers

def parse(length: int,
          tick_delay: int,
          notes: list[Note],
          layers: list[Layer],
          loop_start: int = 0,
          loop: bool = False,) -> Union[list[Union[list, int, str]], str]:
    """
    TODO
    """
    try:
        last_note_id = 0
        sequence = []

        for tick in range(length):
            if loop:
                if tick == loop_start:
                    sequence.append('LOOP')
                    loop = False # Cycle optimization

            for note_id in range(last_note_id, len(notes)):
                last_note_id = note_id
                note = notes[note_id]
                layer = layers[note.layer]
                    
                if note.tick == tick:
                    if layer.lock: continue
                    octave_pitch = get_octave_pitch(note.key, note.pitch)
                    if octave_pitch is None: continue
                    volume = get_volume(
                        note.velocity, layer.volume,
                        note.panning, layer.panning,)
                    
                    element = [
                        BASE_INSTRUMENTS[note.instrument] + octave_pitch[0],
                        octave_pitch[1],
                        volume[0],
                        volume[1],]
                    
                    sequence.append(element)
                    
                else:
                    if type(sequence[-1]) is int:
                        sequence[-1] += tick_delay
                    else:
                        sequence.append(tick_delay)
                    break
        
        return sequence
    
    except Exception.__str__() as ex:
        return ex
 
def get_octave_pitch(key, pitch):
    """
    Based on https://minecraft.fandom.com/wiki/Note_Block#Notes
    """
    key += pitch * 0.01
    octave_range = 1
    
    if (key>=-15) and (key<=8):
        octave_range -= 2
        key -= 12
    elif (key>=9) and (key<=32):
        octave_range -= 1
    elif (key>=33) and (key<=57):
        pass
    elif (key>=58) and (key<=80):
        octave_range += 1
    elif (key>=81) and (key<=105):
        octave_range += 2
        key += 12
    else:
        return None
    
    pitch = round(0.5*2**((key-9-octave_range*24)/12), 6)
    # На фандоме тоже 6 после запятой
    if pitch % 1 == 0.0: pitch = int(pitch)

    if octave_range == 1: octave_range = ''
    else: octave_range = '_' + str(octave_range - 1)
    
    return octave_range, pitch

def get_volume(n_vel, l_vol, n_pan, l_pan):
    """
    Don't even ask me how it works...
    """
    if l_pan == 0:
        lower_bound = -100
        upper_bound = 100
    elif l_pan > 0:
        lower_bound = -100 + l_pan
        upper_bound = 100
    else:
        lower_bound = -100
        upper_bound = 100 + l_pan

    pan = lower_bound + ((n_pan + 100) * (upper_bound - lower_bound) / 200)

    vol = n_vel / 10000 * l_vol

    if pan == 0:
        vol_l = vol_r = vol
    elif pan < 0:
        vol_l = vol
        vol_r = vol * (100 + pan) / 100
    elif pan > 0:
        vol_l = vol * (100 - pan) / 100
        vol_r = vol
    
    vol_l = round(vol_l, 2)
    vol_r = round(vol_r, 2)

    if vol_l % 1 == 0.0: vol_l = int(vol_l)
    if vol_r % 1 == 0.0: vol_r = int(vol_r)

    return vol_l, vol_r

def separate_sequence(sequence: list[list, int]) -> list[list]:
    final = []
    data = []
    current_size = 1 # JSON contains BRACKETS. 1 is for the first [
    file_count = 0
    MAX_SIZE = 25000

    for item in sequence:
        # Items are sepatated with commas. The last one will be replaced with ]
        # 3 is for string quotes and commas ("str",) and 1 is for commas
        item_size = len(str(item).replace(' ', '')) + (3 if (
            type(item) == str) else 1)

        if current_size + item_size > MAX_SIZE:
            final.append(data)
            file_count += 1
            data = []
            current_size = 1
        
        data.append(item)
        current_size += item_size
    
    if data:
        final.append(data)
        file_count += 1
    
    return final, file_count

def dump_data(sepparated_data):
    i = 0
    for element in sepparated_data:
        data = json.dumps(element, separators=(',', ':'))
        with open(file[:-4]+'_'+str(i)+'.json', 'w') as json_result:
            json_result.write(data)
        i += 1
    
    sepparated_data[0][0][0] = i - 1
    data = json.dumps(sepparated_data[0], separators=(',', ':'))
    with open(file[:-4]+'_0.json', 'w') as json_result:
        json_result.write(data)
