import sys
import subprocess
from Flags import FLAGS
from WaveToMidiTranscription import run
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from magenta.models.onsets_frames_transcription import configs
from magenta.models.onsets_frames_transcription import data
from pathlib import Path
from chordsgeneration import main
from NewMelody import main
from ImproviseFurtherwithBach import main
from Improvisefurther import main
import subprocess
import tensorflow.compat.v1 as tf
from config import cfg



class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.filePath=None
        self.midiPath=None
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.buttontranscribe = QPushButton('Transcribe', self)
        self.buttontranscribe.setToolTip('Transcribe the wav data')
        self.buttontranscribe.move(100,70)
        self.buttontranscribe.clicked.connect(self.execute)
        self.buttonfilewav= QPushButton('Select File to transcribe', self)
        self.buttonfilewav.setToolTip('Select the file that you want to transcribe')
        self.buttonfilewav.move(300,70)
        self.buttonfilewav.clicked.connect(self.selectFile)
        self.buttonimprov= QPushButton('Improvise Further', self)
        self.buttonimprov.setToolTip('The AI will generate a new sequence')
        self.buttonimprov.move(100, 100)
        self.buttonimprov.clicked.connect(self.improvise)
        self.buttonbach= QPushButton('Improv by Bach', self)
        self.buttonbach.setToolTip('The AI will generate a new sequence BachStyle')
        self.buttonbach.move(300,100)
        self.buttonbach.clicked.connect(self.bach)
        self.buttonNewMelody = QPushButton ('Create a new Melody', self)
        self.buttonNewMelody.setToolTip('The AI will create a new melody')
        self.buttonNewMelody.move(100,130)
        self.buttonNewMelody.clicked.connect(self.melody)
        self.buttonchords = QPushButton('Harmonize', self)
        self.buttonchords.setToolTip('The AI will create harmonizing chords')
        self.buttonchords.move(300,130)
        self.buttonchords.clicked.connect(self.chords())
        self.buttonsheet=QPushButton('Show Sheet Music', self)
        self.buttonsheet.setToolTip('Opens MuseScore to display Sheet Music')
        self.buttonsheet.move(200,100)
        self.buttonsheet.clicked.connect(self.sheetmusic)

        self.show()


    def execute(self):
        if self.filePath is None:
            QMessageBox.about(self,'No File',"No File was selected, please select a file to transcribe")
        else:
            tf.flags.FLAGS.__delattr__('hparams')
            tf.app.flags.DEFINE_string(
                'hparams', cfg["hparams"],
                'Comma-separated list of `name=value` pairs. For each pair, the value of '
                'the hyperparameter named `name` is set to `value`. This mapping is merged '
                'with the default hyperparameters.')
            tf.flags.FLAGS.__delattr__('config')
            tf.app.flags.DEFINE_string('config', 'onsets_frames',
                                       'Name of the config to use.')
            run(['', self.filePath], config_map=configs.CONFIG_MAP, data_fn=data.provide_batch)
            self.midiPath = self.filePath + '.midi'

    def selectFile(self):
        self.filePath = QFileDialog.getOpenFileName(self, "Open a Wave file", "", "Wave File (*.wav)")[0]

    def improvise(self):
        if self.midiPath is None:
            QMessageBox.about(self, "No file", "No File was selected, please select a Midi file to improvise to")
        else:
            tf.flags.FLAGS.__delattr__('bundle_file')
            tf.app.flags.DEFINE_string(
                'bundle_file', cfg['bundle_file2'],
                'Path to the bundle file. If specified, this will take priority over '
                'run_dir, unless save_generator_bundle is True, in which case both this '
                'flag and run_dir are required')
            main(self.midiPath)
            self.midiPath = self.filePath + '.improv.midi'

    def bach(self):
        if self.midiPath is None:
            QMessageBox.about(self, "No file", "No File was selected, please select a Midi file to improvise to")
        else:
            tf.flags.FLAGS.__delattr__('bundle_file')
            tf.app.flags.DEFINE_string(
                'bundle_file', cfg['bundle_file3'],
                'Path to the bundle file. If specified, this will take priority over '
                'run_dir, unless save_generator_bundle is True, in which case both this '
                'flag and run_dir are required')
            main(self.midiPath)
            self.midiPath = self.filePath + '.bach.midi'

    def melody(self):
        if self.midiPath is None:
            QMessageBox.about(self, "No file", "No File was selected, please select a Midi file to improvise to")
        else:
            tf.flags.FLAGS.__delattr__('hparams')
            tf.flags.FLAGS.__delattr__('config')
            tf.app.flags.DEFINE_string(
                'config',
                cfg['config2'],
                "Which config to use. Must be one of 'basic', 'lookback', or 'attention'. "
                "Mutually exclusive with `--melody_encoder_decoder`.")
            tf.flags.FLAGS.__delattr__('bundle_file')
            tf.app.flags.DEFINE_string(
                'bundle_file', cfg['bundle_file4'],
                'Path to the bundle file. If specified, this will take priority over '
                'run_dir and checkpoint_file, unless save_generator_bundle is True, in '
                'which case both this flag and either run_dir or checkpoint_file are '
                'required')
            main(self.midiPath)
            self.midiPath = self.filePath + '.melody.midi'

    def chords(self):
        if self.midiPath is None:
            QMessageBox.about(self, "No file", "No File was selected, please select a Midi file to improvise to")
        else:
            tf.flags.FLAGS.__delattr__('hparams')
            tf.flags.FLAGS.__delattr__('config')
            tf.app.flags.DEFINE_string(
                'config',
                cfg['config1'],
                "Which config to use. Must be one of 'basic_improv', 'attention_improv', "
                "or 'chord_pitches_improv'.")
            tf.flags.FLAGS.__delattr__('bundle_file')
            tf.app.flags.DEFINE_string(
                'bundle_file', cfg['bundle_file1'],
                'Path to the bundle file. If specified, this will take priority over '
                'run_dir, unless save_generator_bundle is True, in which case both this '
                'flag and run_dir are required')
            main(self.midiPath)
            self.midiPath = self.filePath + '.chords.midi'




    def sheetmusic(self):
        subprocess.run(['C:/Program Files/MuseScore 3/bin/MuseScore3.exe'])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
