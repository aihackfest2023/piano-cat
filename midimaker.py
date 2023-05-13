from basic_pitch.inference import predict_and_save
from datetime import datetime


def record_to_midi(name):
    input_path = [f'static/temp/{name}.mp3']
    output_path = 'static/temp'
    save_midi = True
    sonify_midi = False
    save_model_outputs = False
    save_notes = False
    predict_and_save(input_path, output_path, save_midi, sonify_midi, save_model_outputs, save_notes)
