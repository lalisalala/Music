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
"""Generate polyphonic tracks from a trained checkpoint.

Uses flags to define operation.
"""
import ast
import os
import time

import magenta
from magenta.models.polyphony_rnn import polyphony_model
from magenta.models.polyphony_rnn import polyphony_sequence_generator
from magenta.models.shared import sequence_generator
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
    bundle_file = os.path.expanduser(cfg['bundle_file_bach'])
    return sequence_generator_bundle.read_bundle_file(bundle_file)


def run_with_flags(generator, midi_path=None):
    """Generates polyphonic tracks and saves them as MIDI files.

    Uses the options specified by the flags defined in this module.

    Args:
      generator: The PolyphonyRnnSequenceGenerator to use for generation.
    """
    output_dir = os.path.expanduser(cfg['output_dir'])
    primer_midi = os.path.expanduser(midi_path)

    if not tf.gfile.Exists(output_dir):
        tf.gfile.MakeDirs(output_dir)

    qpm = magenta.music.DEFAULT_QUARTERS_PER_MINUTE
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
    generate_end_time = cfg['num_steps'] * seconds_per_step + 2

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

    generator_options.args['temperature'].float_value = 1.0
    generator_options.args['beam_size'].int_value = 1
    generator_options.args['branch_factor'].int_value = 1
    generator_options.args[
        'steps_per_iteration'].int_value = 1
    generator_options.args['condition_on_primer'].bool_value = (
        True)
    generator_options.args['no_inject_primer_during_generation'].bool_value = (
        not False)

    tf.logging.debug('primer_sequence: %s', primer_sequence)
    tf.logging.debug('generator_options: %s', generator_options)

    # Make the generate request num_outputs times and save the output as midi
    # files.
    date_and_time = time.strftime('%Y-%m-%d_%H%M%S')
    digits = len(str(1))
    for i in range(1):
        generated_sequence = generator.generate(primer_sequence, generator_options)

        midi_filename = primer_midi.replace('midi', 'bach.midi')
        midi_path = os.path.join(output_dir, midi_filename)
        magenta.music.sequence_proto_to_midi_file(generated_sequence, midi_path)

    tf.logging.info('Wrote %d MIDI files to %s',
                    1, output_dir)


def main(unused_argv):
    """Saves bundle or runs generator based on flags."""
    tf.logging.set_verbosity('INFO')

    bundle = get_bundle()

    config_id = bundle.generator_details.id
    config = polyphony_model.default_configs[config_id]
    config.hparams.parse(cfg['hparams'])
    # Having too large of a batch size will slow generation down unnecessarily.
    config.hparams.batch_size = min(
        config.hparams.batch_size, 1)

    generator = polyphony_sequence_generator.PolyphonyRnnSequenceGenerator(
        model=polyphony_model.PolyphonyRnnModel(config),
        details=config.details,
        steps_per_quarter=config.steps_per_quarter,
        checkpoint=None,
        bundle=bundle)

    run_with_flags(generator, unused_argv)


def console_entry_point():
    tf.app.run(main)


if __name__ == '__main__':
    console_entry_point()
