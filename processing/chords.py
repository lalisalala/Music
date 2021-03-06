from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import time
import magenta
from magenta.models.improv_rnn import improv_rnn_model
from magenta.models.improv_rnn import improv_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from magenta.music.protobuf import generator_pb2
from magenta.music.protobuf import music_pb2
import tensorflow.compat.v1 as tf
from config import cfg

CHORD_SYMBOL = music_pb2.NoteSequence.TextAnnotation.CHORD_SYMBOL

# Velocity at which to play chord notes when rendering chords.
CHORD_VELOCITY = 50


def get_bundle():
    """ Gets the bundle from config.py, if you want to change it, go to your config.json and change 'bundle_file_chords'
    Input = None
    Output = None
    """
    bundle_file = os.path.expanduser(cfg['bundle_file_chords'])
    return sequence_generator_bundle.read_bundle_file(bundle_file)


def generate_chords(midi_path=None):
    """Generates harmonizing chords and saves them as MIDI.
    Input parameters : Midi to harmonize to (Primer Midi), automatically set to Midi from transcription.py
    Output = Midifile named "Midifile.chords.midi" in same location
    """

    tf.logging.set_verbosity('INFO')

    bundle = get_bundle()

    if bundle:
        config_id = bundle.generator_details.id
        config = improv_rnn_model.default_configs[config_id]
        config.hparams.parse(cfg['hparams'])

    generator = improv_rnn_sequence_generator.ImprovRnnSequenceGenerator(
        model=improv_rnn_model.ImprovRnnModel(config),
        details=config.details,
        steps_per_quarter=config.steps_per_quarter,
        checkpoint=None,
        bundle=bundle)
    output_dir = os.path.expanduser(cfg['output_dir'])
    primer_midi = os.path.expanduser(midi_path)

    if not tf.gfile.Exists(output_dir):
        tf.gfile.MakeDirs(output_dir)

    qpm = magenta.music.DEFAULT_QUARTERS_PER_MINUTE
    primer_sequence = magenta.music.midi_file_to_sequence_proto(primer_midi)
    qpm = primer_sequence.tempos[0].qpm

    # Create backing chord progression from flags.
    backing_chords = 'C G Am F C G F C'
    raw_chords = backing_chords.split()
    repeated_chords = [chord for chord in raw_chords
                       for _ in range(16)]
    backing_chords = magenta.music.ChordProgression(repeated_chords)

    # Derive the total number of seconds to generate based on the QPM of the
    # priming sequence and the length of the backing chord progression.
    seconds_per_step = 60.0 / qpm / generator.steps_per_quarter
    total_seconds = len(backing_chords) * seconds_per_step

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

    # Add the backing chords to the input sequence.
    chord_sequence = backing_chords.to_sequence(sequence_start_time=0.0, qpm=qpm)
    for text_annotation in chord_sequence.text_annotations:
        if text_annotation.annotation_type == CHORD_SYMBOL:
            chord = input_sequence.text_annotations.add()
            chord.CopyFrom(text_annotation)
    input_sequence.total_time = len(backing_chords) * seconds_per_step

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
        renderer = magenta.music.BasicChordRenderer(velocity=CHORD_VELOCITY)
        renderer.render(generated_sequence)

        midi_filename = primer_midi.replace('midi', 'chords.midi')
        midi_path = os.path.join(cfg['output_dir'], midi_filename)
        magenta.music.sequence_proto_to_midi_file(generated_sequence, midi_path)

    tf.logging.info('Wrote %d MIDI files to %s',
                    1, cfg['output_dir'])


