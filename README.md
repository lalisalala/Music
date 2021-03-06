## lisenta - Automatic Music Transcription

![Screenshot](Piano1.jpg)

A prototype called lisenta that uses Tensorflow and Magenta to detect musical notes in a Piano .wav file. It transcribes it onto a midi file. Additionally, you can choose from a variety of different applications to generate new piano sequences.
##### 1. Hm, what are the notes in this piece?   
This program detects notes and transcribes your piano.wav files into .midi files. It uses Machine Learning for accurate onset detection. Try it out! It's perfect to create sheet paper. Look at 6. for further information.
##### 2. Let this program be creative! 
Need some variety in your songs? Try out the melody generator that creates a new monophonic melody based on one of your .midi songs. 
##### 3. Bach is still alive
You need inspiration on how to continue your melody? This program offers two pre-trained checkpoints, that help you by adding some lines to your existing work. One of them is Bach-style. So prepare for some serious Baroqueness.
##### 4.  Find the harmonizing chords to your melody!
Need some help in finding the right harmonizing chords? This application adds fitting chords to your existing melody. Try out a One-Man-Orchestra.
##### 5. Mix and Match 
Mix and match the applications mentioned above to create your perfect song. You can also run these applications several times to see what this program creates. Just have fun! But careful, since this project is still in its development phase, errors can occure.
##### 6. Show it on Sheet Music
Show whatever madness you just created on sheet paper to share it with others. The program MuseScore is used for this procedure. You can further tweak your creation on this program. 


### Setup
Use `pip -m install tensorflow == 1.15.3` to install the specific version of TensorFlow that is compatible with Magenta.
Then add Magenta by `pip install Magenta`. The version used in this program is 1.3.1. 

Get SoX from the Website: http://sox.sourceforge.net/ (32-Bit works on 64-Bit) and add it to your Path on your Computer. Tutorial for Windows: https://stackoverflow.com/questions/17667491/how-to-use-sox-in-windows 

Downgrade the Numba Library to `0.48.0`. 

Download all the pre-trained models and save them on your computer: 
 1. model_dir: https://storage.googleapis.com/magentadata/models/onsets_frames_transcription/maestro_checkpoint.zip
 2. bundle_file_chords:https: http://download.magenta.tensorflow.org/models/chord_pitches_improv.mag
 3. bundle_file_improv: http://download.magenta.tensorflow.org/models/pianoroll_rnn_nade.mag
 4. bundle_file_bach: http://download.magenta.tensorflow.org/models/polyphony_rnn.mag
 5. bundle_file_melody: http://download.magenta.tensorflow.org/models/attention_rnn.mag
 6. Creating Sheet Music: https://musescore.org/de/download


### Usage
In this GitLab, a config.json.example is included, please fill out all the right paths to your checkpoints and models. I would recommend to set up one folder that contains all the models.
When you have successfully updated all the paths in the config.jason.example, rename it to config.json, in order for the code to utilize it. 
Then run the GUI.py. A simple Graphical User Interface will pop up. 

You can choose to upload a file from your local storage or record seven seconds from your microphone. 
Please make sure you select an existing .wav file before transcribing.
After transcribing you can press the other buttons, to try out the improvisation skills. 

When Python says, that there was an error, you have to restart this GUI, as this GUI will continue, even though an error occurred. 

### FYI
This project is in its prime and far from being fully developed yet. It is a simple, fun tool to play around with. Since the developers of Magenta are still very actively updating their GitHub, this program will most probably show some deprecation warnings.  The algorithm for note detection might not always be 100% accurate. If errors occur, feel free to leave a comment on this GitLab.
I will be trying to frequently update this GitLab. 








