from numpy import sign

import pynbs
import json


# TEMPO
tempo = {
    20.0 : 1,
    10.0 : 2,
    6.67 : 3,
    5.0 : 4,
    4.0 : 5,
    3.33 : 6,
    2.86 : 7,
    2.5 : 8,
    2.22 : 9,
    2.0 : 10,
    1.82 : 11,
    1.67 : 12,
    1.54 : 13,
    1.43 : 14,
    1.33 : 15,
    1.25 : 16,
    1.18 : 17,
    1.11 : 18,
    1.05 : 19,
    1.0 : 20,
}

# BASE INSTRUMENTS
instrument = (
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

# SPECIAL TERMINATORS
terminator = (
    0, # tempo
    1, # show lyrics
)

# FIXME
def parse(nbs_file: str):
    '''
    Parses OpenNBS file that matches with some conditions.\n
    ONBS version must be 5.\n
    The tempo must match with the defined tempo dictionary.
    '''

    try:
        nbs = pynbs.read(nbs_file)
        header = nbs.header
        notes = nbs.notes
        layers = nbs.layers
        last_note_id = 0
        sequence = []
        
        assert header.tempo in tempo.keys()
        
        for tick in range(header.song_length+1):
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
                        note.instrument,
                        pitch_octave[1], 
                        pitch_octave[0],
                        volume[0],
                        volume[1]
                    ]
                    
                    sequence.append(element)
                    
                else:
                    if type(sequence[-1]) is int:
                        print('1')
                        sequence[-1] += tempo[header.tempo]
                    else:
                        sequence.append(tempo[header.tempo])
                    break

                # if delay != 0:
                #     sequence.append(delay * tempo[header.tempo])
                #     delay = 0
        
        return sequence
    
    except Exception as ex:
        return ex

# Based on https://minecraft.fandom.com/wiki/Note_Block#Notes
def set_pitch_octave(key, pitch):
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
    
    pitch = round(0.5*2**((key-9-octave_range*24)/12), 4)
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

#file = 'Queen — Bohemian Rhapsody.nbs'
#file = 'wethands.nbs'
file = 'intro.nbs'
data = parse(file)
data = sepparate_data(data)
dump_data(data)




