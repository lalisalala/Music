from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from magenta.models.onsets_frames_transcription import audio_label_data_utils
from magenta.models.onsets_frames_transcription import infer_util
from magenta.models.onsets_frames_transcription import train_util
from magenta.music import midi_io
from magenta.music.protobuf import music_pb2
import six
import tensorflow.compat.v1 as tf
from config import cfg


def create_example(filename, sample_rate, load_audio_with_librosa):
    """Opens the specified audio file and turns it into a example
    Input and output are all set."""
    wav_data = tf.gfile.Open(filename, 'rb').read()
    example_list = list(
        audio_label_data_utils.process_record(
            wav_data=wav_data,
            sample_rate=sample_rate,
            ns=music_pb2.NoteSequence(),
            # decode to handle filenames with extended characters.
            example_id=six.ensure_text(filename, 'utf-8'),
            min_length=0,
            max_length=-1,
            allow_empty_notesequence=True,
            load_audio_with_librosa=load_audio_with_librosa))
    assert len(example_list) == 1
    return example_list[0].SerializeToString()


def transcribe(argv, config_map, data_fn):
    """Transcribes a Wave File to Midi using the specified dataset
    Input parameter: Wave File to transcribe
    Output: Midifile saved as "Wavefile.midi in the same location"""
    tf.logging.set_verbosity('INFO')

    config = config_map[cfg['config_transcription']]
    hparams = config.hparams
    hparams.parse(cfg['hparams'])
    hparams.batch_size = 1
    hparams.truncated_length_secs = 0

    with tf.Graph().as_default():
        examples = tf.placeholder(tf.string, [None])

        dataset = data_fn(
            examples=examples,
            preprocess_examples=True,
            params=hparams,
            is_training=False,
            shuffle_examples=False,
            skip_n_initial_records=0)

        estimator = train_util.create_estimator(config.model_fn,
                                                os.path.expanduser(cfg['model_dir']),
                                                hparams)

        iterator = dataset.make_initializable_iterator()
        next_record = iterator.get_next()

        with tf.Session() as sess:
            sess.run([
                tf.initializers.global_variables(),
                tf.initializers.local_variables()
            ])

            for filename in argv[1:]:
                tf.logging.info('Starting transcription for %s...', filename)

                # The reason we bounce between two Dataset objects is so we can use
                # the data processing functionality in data.py without having to
                # construct all the Example protos in memory ahead of time or create
                # a temporary tfrecord file.
                tf.logging.info('Processing file...')
                sess.run(iterator.initializer,
                         {examples: [
                             create_example(filename, hparams.sample_rate,
                                            0)]})

                def transcription_data(params):
                    del params
                    return tf.data.Dataset.from_tensors(sess.run(next_record))

                input_fn = infer_util.labels_to_features_wrapper(transcription_data)

                tf.logging.info('Running inference...')
                checkpoint_path = None
                prediction_list = list(
                    estimator.predict(
                        input_fn,
                        checkpoint_path=checkpoint_path,
                        yield_single_examples=False))
                assert len(prediction_list) == 1

                sequence_prediction = music_pb2.NoteSequence.FromString(
                    prediction_list[0]['sequence_predictions'][0])

                midi_filename = filename + '.midi'
                midi_io.sequence_proto_to_midi_file(sequence_prediction, midi_filename)

                tf.logging.info('Transcription written to %s.', midi_filename)