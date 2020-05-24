## Automatic Music Transcription
A code that uses Tensorflow and Magenta to detect musical notes in a Piano .wav file. Furthermore, it uses MuseScore to generate Sheet Music.

###Setup
Use `pip -m install tensorflow == 1.15.3` to install the specific version of TensorFlow that is compatible with Magenta.
Then add Magenta by `pip install Magenta`. The current version should be 1.3.1. 

Get SoX from the Website: http://sox.sourceforge.net/ (32-Bit works on 64-Bit) and add it to your Path on your Computer. Tutorial for Windows: https://stackoverflow.com/questions/17667491/how-to-use-sox-in-windows 

Downgrade the Numba Library to `0.48.0`. 

 Please download and unzip the checkpoint from:
https://github.com/tensorflow/magenta/tree/master/magenta/models/onsets_frames_transcription (scroll down to Transcription Script).

### Usage

Use the command line to run this command in WaveToMidiTranscription.py: 
`WaveToMidiTranscription.py --model_dir="path to your maestro_checkpoint file ending with /train" <Path to your input .wav file> --hparams=use_cudnn=false`
                                                            
for example: 
`WaveToMidiTranscription.py --model_dir="C:/Users/Example/Downloads/maestro_checkpoint/train" C:/Users/Example/Downloads/Piano7.wav --hparams=use_cudnn=false`

The code will save the MIDI file in the same directory as your input.
When running from PyCharm, you can type in the parameters in the Configuration Settings. 
Type in: `--model_dir="C:/...../train" C:/Users/.../.wav --hparams=use_cudnn=false` and then hit RUN.

###Sheet Music Generation

In order to generate Sheet Music from the Midi file, please download MuseScore from: https://musescore.org/de/download/musescore.msi and open the MIDI file there.




