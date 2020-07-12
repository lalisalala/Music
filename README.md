## Automatic Music Transcription
A code that uses Tensorflow and Magenta to detect musical notes in a Piano .wav file. It transcribes it onto a midi file. Additionally, you can choose from a variety of different applications:
##### 1. What notes are these?  
This program can transcribe your piano.wav files into .midi files. It uses Machine Learning for accurate note detection. Try it out! It's perfect to create sheet paper. Look at 6. for further information.
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
Then add Magenta by `pip install Magenta`. The current version should be 1.3.1. 

Get SoX from the Website: http://sox.sourceforge.net/ (32-Bit works on 64-Bit) and add it to your Path on your Computer. Tutorial for Windows: https://stackoverflow.com/questions/17667491/how-to-use-sox-in-windows 

Downgrade the Numba Library to `0.48.0`. 

Download all the pre-trained models and save them on your computer: 
 1. Transcription: https://github.com/tensorflow/magenta/tree/master/magenta/models/onsets_frames_transcription (scroll down to Transcription Script, press on "checkpoint")
 2. Melody Generation: https://github.com/magenta/magenta/tree/master/magenta/models/melody_rnn (attention_rnn model) 
 3. Improvising Further: https://github.com/magenta/magenta/tree/master/magenta/models/pianoroll_rnn_nade (Get the pianoroll_rnn_nade model) 
 4. Bach Improvising: https://github.com/magenta/magenta/tree/master/magenta/models/polyphony_rnn (polyphony_rnn model)
 5. Harmonizing Chords: https://github.com/magenta/magenta/tree/master/magenta/models/improv_rnn (chord_pitches_improv model)
 6. Creating Sheet Music: Download MuseScore3 from https://musescore.org/de/download/musescore.msi 


### Usage
In this GitLab, a config.json.example is included, please fill out all the right paths to your checkpoints and models. I would recommend to set up one folder that contains all the models.
When you have successfully updated all the paths in the config.jason.example, rename it to config.json, in order for the code to utilize it. 
Then run the GUI.py. A simple Graphical User Interface will pop up. Please make sure you select an existing .wav file before transcribing.
After transcribing you can press the other buttons, to try out the improvisation skills. 

When your Python Code says, that there was an error, you have to restart this GUI, as this GUI will continue, even though an error occurred. 

### FYI
This project is in its prime and far from being fully developed yet. It is a simple, fun tool to play around with. The algorithm for note detection might not always be 100% accurate. If errors occur, feel free to leave a comment on this GitLab.
I will be trying to frequently update this GitLab.   








