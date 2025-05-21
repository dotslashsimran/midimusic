import subprocess
import os

soundfont = os.path.join(os.getcwd(), "soundfonts", "FluidR3_GM", "FluidR3_GM.sf2")

def midi_to_wav(midi_path, wav_path):

    if not os.path.exists(soundfont):
        raise FileNotFoundError("SoundFont not found. Update the path in audio_converter.py")

    subprocess.run([
        'fluidsynth', '-ni',
        soundfont,
        midi_path,
        '-F', wav_path,
        '-r', '44100'
    ], check=True)