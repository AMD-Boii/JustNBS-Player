import pynbs


def parse(nbs_file):
    #try:
        nbs = pynbs.read(nbs_file)
        header = nbs.header
        notes = nbs.notes
        layers = nbs.layers
        #cust_instruments = nbs.instruments
        last_note = delay = 0
        delay_seq = pitch_seq = instr_seq = vol_seq = ''

        print(header)
        pass
        
        for tick in range(header.song_length+1):
            for note_id in range(last_note, len(notes)):
                last_note = note_id
                note = notes[note_id]
                layer = layers[note.layer]
                        
                if note.tick == tick:
                    if layer.lock: continue
                    #volume = set_volume(note.velocity, note.panning,
                    #                    layer.volume, layer.panning)
                    volume = 100
                    if volume < 10: continue
                    pitch = set_pitch(note.key, note.pitch)
                    if pitch is None: continue

                    #delay_seq.append(delay)
                    #print(tick, delay, pitch, volume)
                    delay = 0
                else:
                    delay += 1
                    break

        with open(nbs_file[:-4]+'.del', 'w') as delay_f:
            delay_f.write(delay_seq)
        
        with open(nbs_file[:-4]+'.pit', 'w') as pitch_f:
            pitch_f.write(pitch_seq)

        with open(nbs_file[:-4]+'.vol', 'w') as volume_f:
            volume_f.write(vol_seq)
        
        with open(nbs_file[:-4]+'.ins', 'w') as instrument_f:
            instrument_f.write(instr_seq)

# Based on https://minecraft.fandom.com/wiki/Note_Block#Notes
def set_pitch(key, pitch):
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
    
    pitch = 0.5*2**((key-9-octave_range*24)/12)
    #if octave_range == 1: octave_range = ''
    #else: octave_range = '_' + str(octave_range - 1)
    
    #return [octave_range, pitch]
    return pitch

def set_volume(note_vel, note_pann, layer_vol, layer_pann):

    volume_L = 1
    volume_R = 1

    return [volume_L, volume_R]


parse('Queen — Bohemian Rhapsody.nbs')
