from midi2audio import FluidSynth


def synthesize(title, font):
    fs = FluidSynth()
    fs.sound_font = font
    fs.midi_to_audio(f'static/temp/{title}.mid', f'static/temp/sm_{title}.mp3')

#synthesize('h2h2', 'soundfont/FluidR3_GM.sf2')
