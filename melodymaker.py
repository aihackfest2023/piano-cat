from note_seq import midi_io
import note_seq
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2


def convert(midi):
    notes = midi_io.midi_file_to_note_sequence(midi)
    return notes


def generate(title, temp, duration):
    bundle = sequence_generator_bundle.read_bundle_file('mag/basic_rnn.mag')
    generator_map = melody_rnn_sequence_generator.get_generator_map()
    melody_rnn = generator_map['basic_rnn'](checkpoint=None, bundle=bundle)
    melody_rnn.initialize()

    input_sequence = convert(f'static/temp/{title}_basic_pitch.mid')

    num_steps = 256
    if duration > 15:
        adds = int(duration // 15)
        num_steps = pow(2, (8 + adds))
    temperature = temp

    last_end_time = (max(n.end_time for n in input_sequence.notes)
                     if input_sequence.notes else 0)
    qpm = input_sequence.tempos[0].qpm
    seconds_per_step = 30.0 / qpm / melody_rnn.steps_per_quarter
    total_seconds = num_steps * seconds_per_step

    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generator_options.generate_sections.add(
        start_time=last_end_time + seconds_per_step,
        end_time=total_seconds)

    sequence = melody_rnn.generate(input_sequence, generator_options)

    note_seq.sequence_proto_to_midi_file(sequence, f'static/temp/{title}.mid')
