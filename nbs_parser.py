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



def parse(nbs_file):
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
                        note.velocity, layer.volume
                    )
                    if volume <= 0: continue
                    pitch_octave = set_pitch_octave(note.key, note.pitch)
                    if pitch_octave is None: continue
                    panning = set_panning(note.panning, layer.panning)

                    element = [0, 0, 0, 0]
                    element[0] = str(
                        instrument[note.instrument] +
                        pitch_octave[1]
                    )
                    element[1] = pitch_octave[0]
                    element[2] = volume
                    element[3] = panning
                    
                    sequence.append(element)

                else:
                    sequence.append(terminator[0])
                    break
        
        print(len(str(sequence)))
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
    if octave_range == 1: octave_range = ''
    else: octave_range = '_' + str(octave_range - 1)
    
    return (pitch, octave_range)

def set_volume(n_vel, l_vol):
    vol = round(n_vel / 10000 * l_vol, 2)
    return vol

def set_panning(n_pan, l_pan):
    if n_pan == 0 or l_pan == 0:
        return round(n_pan, 2)
    elif n_pan > 0:
        return round(min(100, n_pan + l_pan), 2)
    else:
        return round(max(-100, n_pan + l_pan), 2)

def sepparate_data(data):
    final = []
    for value in data:
        if len(str(data).replace(' ', '')) < 24990:
            data.append(value)
        else:
            final.append(data)
            data = []

    return final

def dump_data(data):
    i = 0
    for element in data:
        element = json.dumps(data, separators=(',', ':'))
        with open(file[:-4]+'_'+str(i)+'.json', 'w') as json_result:
            json_result.write(data)
        i += 1

file = 'Queen — Bohemian Rhapsody.nbs'
data = []





