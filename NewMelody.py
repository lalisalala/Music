# Copyright 2020 The Magenta Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Generate melodies from a trained checkpoint of a melody RNN model."""
import ast
import os
import time

import magenta
from magenta.models.melody_rnn import melody_rnn_config_flags
from magenta.models.melody_rnn import melody_rnn_model
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator
from magenta.models.shared import sequence_generator_bundle
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
    bundle_file = os.path.expanduser(cfg['bundle_file_melody'])
    return sequence_generator_bundle.read_bundle_file(bundle_file)


def run_with_flags(generator, midi_path=None):
    """Generates melodies and saves them as MIDI files.

    Uses the options specified by the flags defined in this module.

    Args:
      generator: The MelodyRnnSequenceGenerator to use for generation.
    """
    output_dir = os.path.expanduser(cfg['output_dir'])
    primer_midi = os.path.expanduser(midi_path)

    if not tf.gfile.Exists(output_dir):
        tf.gfile.MakeDirs(output_dir)

    qpm = magenta.music.DEFAULT_QUARTERS_PER_MINUTE
    primer_sequence = magenta.music.midi_file_to_sequence_proto(primer_midi)
    if primer_sequence.tempos and primer_sequence.tempos[0].qpm:
        qpm = primer_sequence.tempos[0].qpm

    # Derive the total number of seconds to generate based on the QPM of the
    # priming sequence and the num_steps flag.
    seconds_per_step = 60.0 / qpm / generator.steps_per_quarter
    total_seconds = cfg['num_steps'] * seconds_per_step + len(primer_midi)

    # Specify start/stop time for generation based on starting generation at the
    # end of the priming sequence and continuing until the sequence is num_steps
    # long.
    generator_options = generator_pb2.GeneratorOptions()
    if primer_sequence:
        input_sequence = primer_sequence
        # Set the start time to begin on the next step after the last note ends.
        if primer_sequence.notes:
            last_end_time = max(n.end_time for n in primer_sequence.notes)
        else:
            last_end_time = 0
        generate_section = generator_options.generate_sections.add(
            start_time=last_end_time + seconds_per_step,
            end_time=total_seconds)

        if generate_section.start_time >= generate_section.end_time:
            tf.logging.fatal(
                'Priming sequence is longer than the total number of steps '
                'requested: Priming sequence length: %s, Generation length '
                'requested: %s',
                generate_section.start_time, total_seconds)
            return
    else:
        input_sequence = music_pb2.NoteSequence()
        input_sequence.tempos.add().qpm = qpm
        generate_section = generator_options.generate_sections.add(
            start_time=0,
            end_time=total_seconds)
    generator_options.args['temperature'].float_value = 1.0
    generator_options.args['beam_size'].int_value = 1
    generator_options.args['branch_factor'].int_value = 1
    generator_options.args[
        'steps_per_iteration'].int_value = 1
    tf.logging.debug('input_sequence: %s', input_sequence)
    tf.logging.debug('generator_options: %s', generator_options)

    # Make the generate request num_outputs times and save the output as midi
    # files.
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    digits = len(str(1))
    for i in range(1):
        generated_sequence = generator.generate(input_sequence, generator_options)

        midi_filename = primer_midi.replace('midi', 'melody.midi')
        midi_path = os.path.join(output_dir, midi_filename)
        magenta.music.sequence_proto_to_midi_file(generated_sequence, midi_path)

    tf.logging.info('Wrote %d MIDI files to %s',
                    1, output_dir)


def main(unused_argv):
    """Saves bundle or runs generator based on flags."""
    tf.logging.set_verbosity('INFO')

    bundle = get_bundle()

    if bundle:
        config_id = bundle.generator_details.id
        config = melody_rnn_model.default_configs[config_id]
        config.hparams.parse(cfg['hparams'])

    generator = melody_rnn_sequence_generator.MelodyRnnSequenceGenerator(
        model=melody_rnn_model.MelodyRnnModel(config),
        details=config.details,
        steps_per_quarter=config.steps_per_quarter,
        checkpoint=None,
        bundle=bundle)

    run_with_flags(generator, unused_argv)


def console_entry_point():
    tf.app.run(main)


if __name__ == '__main__':
    console_entry_point()
