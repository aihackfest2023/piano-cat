from . import midimaker
from . import melodymaker
from . import mp3maker
from mutagen.mp3 import MP3


def duration(filename):
    audio = MP3(f'static/temp/{filename}.mp3')
    print(audio.info.length)
    return audio.info.length


def maker(filename):
    midimaker.record_to_midi(filename)
    melodymaker.generate(filename, 24, duration(filename))
    mp3maker.synthesize(filename, 'soundfont/FluidR3_GM.sf2')

    print("completed!")
