import tensorflow.compat.v1 as tf
from config import cfg


FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('config', 'onsets_frames',
                           'Name of the config to use.')
tf.app.flags.DEFINE_string('model_dir', cfg['model_dir'], 'Path to look for acoustic checkpoints.')
tf.app.flags.DEFINE_string(
    'checkpoint_path', None,
    'Filename of the checkpoint to use. If not specified, will use the latest '
    'checkpoint')
tf.app.flags.DEFINE_boolean(
    'load_audio_with_librosa', False,
    'Whether to use librosa for sampling audio (required for 24-bit audio)')
tf.app.flags.DEFINE_string(
    'run_dir', None,
    'Path to the directory where the latest checkpoint will be loaded from.')
tf.app.flags.DEFINE_string(
    'bundle_file', cfg['bundle_file2'],
    'Path to the bundle file. If specified, this will take priority over '
    'run_dir, unless save_generator_bundle is True, in which case both this '
    'flag and run_dir are required')
tf.app.flags.DEFINE_boolean(
    'save_generator_bundle', False,
    'If true, instead of generating a sequence, will save this generator as a '
    'bundle file in the location specified by the bundle_file flag')
tf.app.flags.DEFINE_string(
    'bundle_description', None,
    'A short, human-readable text description of the bundle (e.g., training '
    'data, hyper parameters, etc.).')
tf.app.flags.DEFINE_string(
    'output_dir', cfg['output_dir'],
    'The directory where MIDI files will be saved to.')
tf.app.flags.DEFINE_integer(
    'num_outputs', 1,
    'The number of tracks to generate. One MIDI file will be created for '
    'each.')
tf.app.flags.DEFINE_integer(
    'num_steps', 128,
    'The total number of steps the generated track should be, priming '
    'track length + generated steps. Each step is a 16th of a bar.')
tf.app.flags.DEFINE_string(
    'primer_pitches', '',
    'A string representation of a Python list of pitches that will be used as '
    'a starting chord with a quarter note duration. For example: '
    '"[60, 64, 67]"')
tf.app.flags.DEFINE_string(
    'primer_melody', '',
    'A string representation of a Python list of '
    'magenta.music.Melody event values. For example: '
    '"[60, -2, 60, -2, 67, -2, 67, -2]".')
tf.app.flags.DEFINE_string(
    'primer_pianoroll', '',
    'A string representation of a Python list of '
    '`magenta.music.PianorollSequence` event values (tuples of active MIDI'
    'pitches for a sequence of steps). For example: '
    '"[(55,), (54,), (55, 53), (50,), (62, 52), (), (63, 55)]".')
tf.app.flags.DEFINE_string(
    'primer_midi', '',
    'The path to a MIDI file containing a polyphonic track that will be used '
    'as a priming track.')
tf.app.flags.DEFINE_boolean(
    'condition_on_primer', True,
    'If set, the RNN will receive the primer as its input before it begins '
    'generating a new sequence.')
tf.app.flags.DEFINE_boolean(
    'inject_primer_during_generation', False,
    'If set, the primer will be injected as a part of the generated sequence. '
    'This option is useful if you want the model to harmonize an existing '
    'melody.')
tf.app.flags.DEFINE_float(
    'qpm', None,
    'The quarters per minute to play generated output at. If a primer MIDI is '
    'given, the qpm from that will override this flag. If qpm is None, qpm '
    'will default to 60.')
tf.app.flags.DEFINE_integer(
    'beam_size', 1,
    'The beam size to use for beam search when generating tracks.')
tf.app.flags.DEFINE_integer(
    'branch_factor', 1,
    'The branch factor to use for beam search when generating tracks.')
tf.app.flags.DEFINE_string(
    'log', 'INFO',
    'The threshold for what messages will be logged DEBUG, INFO, WARN, ERROR, '
    'or FATAL.')
tf.app.flags.DEFINE_string(
    'hparams', cfg["hparams"],
    'Comma-separated list of `name=value` pairs. For each pair, the value of '
    'the hyperparameter named `name` is set to `value`. This mapping is merged '
    'with the default hyperparameters.')
tf.app.flags.DEFINE_integer(
    'steps_per_chord', 16,
    'The number of melody steps to take per backing chord. Each step is a 16th '
    'of a bar, so if backing_chords = "C G Am F" and steps_per_chord = 16, '
    'four bars will be generated.')
tf.app.flags.DEFINE_string(
    'backing_chords', 'C G Am F C G F C',
    'A string representation of a chord progression, with chord symbols '
    'separated by spaces. For example: "C Dm7 G13 Cmaj7". The duration of each '
    'chord, in steps, is specified by the steps_per_chord flag.')
tf.app.flags.DEFINE_float(
    'temperature', 1.0,
    'The randomness of the generated melodies. 1.0 uses the unaltered softmax '
    'probabilities, greater than 1.0 makes melodies more random, less than 1.0 '
    'makes melodies less random.')
tf.app.flags.DEFINE_integer(
    'steps_per_iteration', 1,
    'The number of melody steps to take per beam search iteration.')