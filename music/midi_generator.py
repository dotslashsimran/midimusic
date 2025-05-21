from midiutil import MIDIFile
import colorsys

def rgb_to_hue(r, g, b):
    h, _, _ = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h * 360

def generate_midi_from_image(image, output_path):
    width, height = image.size
    pixels = image.load()

    midi = MIDIFile(3) 
    midi.addTempo(0, 0, 100)
    midi.addTempo(1, 0, 100)
    midi.addTempo(2, 0, 100)

    midi.addProgramChange(0, 0, 0, 40)  # melody: violin
    midi.addProgramChange(1, 0, 0, 24)  # harmony: guitar

    time_counter = 0
    beat_interval = 0.5  

    for x in range(0, width, 3):  
        note_found = False
        for y in range(height):
            r, g, b = pixels[x, y]
            brightness = 0.299 * r + 0.587 * g + 0.114 * b

            if brightness < 230:
                hue = rgb_to_hue(r, g, b)
                pitch = 60 + (height - y) // 6
                duration = 0.4 + (x % 5) * 0.1
                velocity = 60 + (x % 40)

                if 0 <= hue < 60:
                    track = 0  
                elif 60 <= hue < 180:
                    track = 1  
                else:
                    track = 0

                midi.addNote(track, channel=0, pitch=pitch,
                             time=time_counter, duration=duration, volume=velocity)
                note_found = True
                break
        if note_found:
            time_counter += beat_interval

    for i in range(16):
        t = i * beat_interval
        if i % 4 == 0:
            midi.addNote(2, 9, 36, t, 0.3, 100)  # Kick
        if i % 4 == 2:
            midi.addNote(2, 9, 38, t, 0.3, 80)   # Snare
        midi.addNote(2, 9, 42, t, 0.2, 50)       # Hi-hat

    with open(output_path, 'wb') as f:
        midi.writeFile(f)

    return True