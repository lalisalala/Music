## Automatic Music Transcription
A code that uses Tensorflow and Magenta to detect musical notes in a Piano .wav file. It transcribes it onto a midi file. Additionally, you can choose from a variety of different applications:
##### 1. Let this program be creative! 
Need some variety in your songs? Try out the melody generator that creates a new monophonic melody based on one of your .midi songs. 
##### 2. Bach is still alive
You need inspiration on how to continue your melody? This program offers two pre-trained checkpoints, that help you by adding some lines to your existing work. One of them is Bach-style. So prepare for some serious Baroqueness.
##### 2.  Find the harmonizing chords to your melody
Need some help in finding the right harmonizing chords? This application adds fitting chords to your existing melody. Try out a One-Man-Orchestra.
##### 3. Mix and Match 
Mix and match the applications mentioned above to create your perfect song. You can also run these applications several times to see what this program creates. Just have fun!
##### 4. Show it on Sheet Music
Show whatever madness you just created on sheet paper to share it with others. The program MuseScore is used for this procedure. You can further tweak your creation on this program. Others will love to read this.

### Setup
Use `pip -m install tensorflow == 1.15.3` to install the specific version of TensorFlow that is compatible with Magenta.
Then add Magenta by `pip install Magenta`. The current version should be 1.3.1. 

Get SoX from the Website: http://sox.sourceforge.net/ (32-Bit works on 64-Bit) and add it to your Path on your Computer. Tutorial for Windows: https://stackoverflow.com/questions/17667491/how-to-use-sox-in-windows 

Downgrade the Numba Library to `0.48.0`. 

### Usage

#### Music Transcription 
First please download and unzip the checkpoint from:
https://github.com/tensorflow/magenta/tree/master/magenta/models/onsets_frames_transcription (scroll down to Transcription Script).

Use the command line to run this command in WaveToMidiTranscription.py: 
`WaveToMidiTranscription.py --model_dir="path to your maestro_checkpoint file ending with /train" <Path to your input .wav file> --hparams=use_cudnn=false`
                                                            
for example: 
`WaveToMidiTranscription.py --model_dir="C:/Users/Example/Downloads/maestro_checkpoint/train" C:/Users/Example/Downloads/Piano7.wav --hparams=use_cudnn=false`

The code will save the MIDI file in the same directory as your input.
When running from PyCharm, you can type in the parameters in the Configuration Settings. 
Type in: `--model_dir="C:/...../train" C:/Users/.../.wav --hparams=use_cudnn=false` and then hit RUN.

### Sheet Music Generation

In order to generate Sheet Music from the Midi file, please download MuseScore from: https://musescore.org/de/download/musescore.msi and open the MIDI file there.




