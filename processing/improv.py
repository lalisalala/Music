import os
import time
import magenta
from magenta.models.shared import sequence_generator_bundle
from magenta.music import constants
from magenta.music.protobuf import generator_pb2
from magenta.music.protobuf import music_pb2
import tensorflow.compat.v1 as tf
from config import cfg


def get_bundle():
    """Returns a generator_pb2.GeneratorBundle object based read from bundle_file.

    Returns:
      Either a generator_pb2.GeneratorBundle or None if the bundle_file flag is
      not set or the save_generator_bundle flag is set.
    """
    bundle_file = os.path.expanduser(cfg['bundle_file_improv'])
    return sequence_generator_bundle.read_bundle_file(bundle_file)


def run_with_flags(generator, midi_path=None):
    """Generates pianoroll tracks and saves them as MIDI files.

    Uses the options specified by the flags defined in this module.

    Args:
      generator: The PianorollRnnNadeSequenceGenerator to use for generation.
    """

    output_dir = os.path.expanduser(cfg['output_dir'])
    primer_midi = os.path.expanduser(midi_path)

    if not tf.gfile.Exists(output_dir):
        tf.gfile.MakeDirs(output_dir)

    qpm = 60
    primer_sequence = magenta.music.midi_file_to_sequence_proto(primer_midi)
    if primer_sequence.tempos and primer_sequence.tempos[0].qpm:
        qpm = primer_sequence.tempos[0].qpm
    else:
        tf.logging.warning(
            'No priming sequence specified. Defaulting to empty sequence.')
        primer_sequence = music_pb2.NoteSequence()
        primer_sequence.tempos.add().qpm = qpm
        primer_sequence.ticks_per_quarter = constants.STANDARD_PPQ

    # Derive the total number of seconds to generate.
    seconds_per_step = 60.0 / qpm / generator.steps_per_quarter
    generate_end_time = cfg['num_steps'] * seconds_per_step

    # Specify start/stop time for generation based on starting generation at the
    # end of the priming sequence and continuing until the sequence is num_steps
    # long.
    generator_options = generator_pb2.GeneratorOptions()
    # Set the start time to begin when the last note ends.
    generate_section = generator_options.generate_sections.add(
        start_time=primer_sequence.total_time,
        end_time=generate_end_time)

    if generate_section.start_time >= generate_section.end_time:
        tf.logging.fatal(
            'Priming sequence is longer than the total number of steps '
            'requested: Priming sequence length: %s, Total length '
            'requested: %s',
            generate_section.start_time, generate_end_time)
        return

    generator_options.args['beam_size'].int_value = 1
    generator_options.args['branch_factor'].int_value = 1

    tf.logging.info('primer_sequence: %s', primer_sequence)
    tf.logging.info('generator_options: %s', generator_options)

    # Make the generate request num_outputs times and save the output as midi
    # files.
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    digits = len(str(1))
    for i in range(1):
        generated_sequence = generator.generate(primer_sequence, generator_options)

        midi_filename = primer_midi.replace('midi', 'improv.midi')
        midi_path = os.path.join(output_dir, midi_filename)
        magenta.music.sequence_proto_to_midi_file(generated_sequence, midi_path)

    tf.logging.info('Wrote %d MIDI files to %s',
                    1, output_dir)
