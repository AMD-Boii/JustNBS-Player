# Released under the MIT License. See LICENSE for details.
#
"""Parser."""

from __future__ import annotations
from typing import Optional, Union

from io import BytesIO

import pynbs
import json
import datetime

TEMPO = (
    20.0, 10.0, 6.67, 5.0, 4.0,
    3.33, 2.86, 2.5, 2.22, 2.0,
    1.82, 1.67, 1.54, 1.43, 1.33,
    1.25, 1.18, 1.11, 1.05, 1.0,
    # 0.95, 0.91, 0.87, 0.83, 0.8,
    # 0.77, 0.74, 0.71, 0.69, 0.67,
    # 0.65, 0.62, 0.61, 0.59, 0.57,
    # 0.56, 0.54, 0.53, 0.51, 0.5,
)

NOTE_BLOCK_VAR = 'block.note_block.'

BASE_INSTRUMENTS = (
    'harp',
    'bass',
    'basedrum',
    'snare',
    'hat',
    'guitar',
    'flute',
    'bell',
    'chime',
    'xylophone',
    'iron_xylophone',
    'cow_bell',
    'didgeridoo',
    'bit',
    'banjo',
    'pling',
)


def get_metadata(nbs_file: BytesIO) -> Union[tuple, str]:
    '''
    Reads metadata from the NBS file, checks conditions\n
    and returns header and NBS data for further parsing\n
    if matches these conditions.
    '''
    try:
        try:
            nbs_data = pynbs.Parser(nbs_file).read_file()
        except Exception:
            return 'Неверный или поврежденный файл!'
        
        header = nbs_data.header

        #print(header.tempo)

        #assert header.version == 5, 'Неподдерживаемая версия NBS!'
        #assert header.tempo in TEMPO, 'Неподдерживаемый темп!'

        #length = header.song_length * (TEMPO.index(header.tempo) + 1)
        #duration = str(datetime.timedelta(seconds=length // 20))

        notes = nbs_data.notes
        layers = nbs_data.layers

        return header, notes, layers
    
    except AssertionError as assertion:
        return assertion.__str__()

def parse(length: int,
          tempo: int,
          notes: list[pynbs.Note],
          layers: list[pynbs.Layer]) -> Union[list[Union[list, int]], str]:
    '''
    Parses NBS data (notes, layers) and outputs a list of\n
    JSON-ready list that contains lists of every single\n
    note parameters and delays.
    '''
    try:
        last_note_id = 0
        sequence = []

        for tick in range(length):
            for note_id in range(last_note_id, len(notes)):
                last_note_id = note_id
                note = notes[note_id]
                layer = layers[note.layer]
                    
                if note.tick == tick:
                    if layer.lock: continue
                    volume = set_volume(
                        note.velocity, layer.volume,
                        note.panning, layer.panning
                    )
                    pitch_octave = set_pitch_octave(note.key, note.pitch)
                    if pitch_octave is None: continue
                    
                    element = [
                        NOTE_BLOCK_VAR + BASE_INSTRUMENTS[note.instrument] + pitch_octave[1],
                        pitch_octave[0],
                        volume[0],
                        volume[1]
                    ]
                    
                    sequence.append(element)
                    
                else:
                    if type(sequence[-1]) is int:
                        sequence[-1] += tempo #TEMPO[header.tempo]
                    else:
                        sequence.append(tempo) #TEMPO[header.tempo])
                    break
        
        return sequence
    
    except Exception as ex:
        return ex
 
def set_pitch_octave(key, pitch):
    '''
    Based on https://minecraft.fandom.com/wiki/Note_Block#Notes
    '''
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
    
    pitch = round(0.5*2**((key-9-octave_range*24)/12), 8)
    if pitch % 1 == 0.0: pitch = int(pitch)
    if octave_range == 1: octave_range = ''
    else: octave_range = '_' + str(octave_range - 1)
    
    return (pitch, octave_range)

def set_volume(n_vel, l_vol, n_pan, l_pan):
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

    return (vol_l, vol_r)

# FIXME оптимизация проверки на кол-во символов
def sepparate_data(raw_data: list[list, int]) -> list[list]:
    final = []
    data = []
    counter = 0
    didLastAppend = False

    while counter < len(raw_data):
        if len(str(data).replace(' ', '')) < 25000:
            data.append(raw_data[counter])
            didLastAppend = False
            
            if len(str(data).replace(' ', '')) >= 25000:
                data.pop()
                final.append(data)
                data = []
                didLastAppend = True
            else:
                counter += 1
        else:
            final.append(data)
            data = []
            didLastAppend = True

    if not didLastAppend: final.append(data)
    
    return final

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


# file = 'Queen — Bohemian Rhapsody.nbs'
# file = 'show.nbs'
# file = 'intro.nbs'
# data = parse(file)
# data = separate_data(data)
# dump_data(data)

# with open('test.nbs', "rb") as fileobj:
#     print(get_metadata(fileobj))


