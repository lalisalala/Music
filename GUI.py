import sys
import subprocess
from Flags import FLAGS
from WaveToMidiTranscription import run
from PyQt5.QtCore import pyqtSlot, QSize, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QImage, QPalette, QBrush
from magenta.models.onsets_frames_transcription import configs
from magenta.models.onsets_frames_transcription import data
import pathlib
from Improvisefurther import main
from ImproviseFurtherwithBach import main as main1
from NewMelody import main as main2
from chordsgeneration import main as main3
import subprocess
from config import cfg
from Micro import record




class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Automatic Music Transcription and Generation'
        self.left = 30
        self.top = 30
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
        self.buttontranscribe.move(350,100)
        self.buttontranscribe.clicked.connect(self.execute)
        self.buttonfilewav= QPushButton('Select File to Transcribe', self)
        self.buttonfilewav.setToolTip('Select the file that you want to transcribe')
        self.buttonfilewav.move(0,0)
        self.buttonfilewav.clicked.connect(self.selectFile)
        self.buttonmicro = QPushButton('Record Your Piece', self)
        self.buttonmicro.setToolTip('Records 5 seconds')
        self.buttonmicro.move(200,0)
        self.buttonmicro.clicked.connect(self.record)
        self.buttonimprov= QPushButton('Improvise Further', self)
        self.buttonimprov.setToolTip('The AI will generate a New Sequence')
        self.buttonimprov.move(180, 190)
        self.buttonimprov.clicked.connect(self.improvise)
        self.buttonbach= QPushButton('Improv by Bach', self)
        self.buttonbach.setToolTip('The AI will generate a New Sequence BachStyle')
        self.buttonbach.move(300,130)
        self.buttonbach.clicked.connect(self.bach)
        self.buttonNewMelody = QPushButton ('Create a New Melody', self)
        self.buttonNewMelody.setToolTip('The AI will create a new melody')
        self.buttonNewMelody.move(230,160)
        self.buttonNewMelody.clicked.connect(self.melody)
        self.buttonchords = QPushButton('Harmonize', self)
        self.buttonchords.setToolTip('The AI will create harmonizing chords')
        self.buttonchords.move(125, 220)
        self.buttonchords.clicked.connect(self.chords)
        self.buttonsheet=QPushButton('Show Sheet Music', self)
        self.buttonsheet.setToolTip('Opens MuseScore to display Sheet Music')
        self.buttonsheet.move(530,450)
        self.buttonsheet.clicked.connect(self.sheetmusic)
        self.buttonmidi=QPushButton ('Select a Midi file', self)
        self.buttonmidi.setToolTip('Select a Midi File that you want to process')
        self.buttonmidi.move(120,0)
        self.buttonmidi.clicked.connect(self.selectMidi)
        picture = QImage('Piano1.jpg')
        spicture = picture.scaled(QSize(640,480))
        palette = QPalette()
        palette.setBrush(10, QBrush(spicture))
        self.setPalette(palette)


        self.show()


    def execute(self):
        if self.filePath is None:
            QMessageBox.about(self,'No File',"No File was selected, please select a file to transcribe")
        else:
            run(['', self.filePath], config_map=configs.CONFIG_MAP, data_fn=data.provide_batch)
            self.midiPath = self.filePath + '.midi'
            QMessageBox.about(self,'Success!', 'Transcription was successful, the Midi was written to ' + self.midiPath)

    def selectFile(self):
        self.filePath = QFileDialog.getOpenFileName(self, "Open a Wave file", "", "Wave File (*.wav)")[0]

    def selectMidi(self):
        self.midiPath = QFileDialog.getOpenFileName(self, "Open a Midi File", "", "Midi File (*.midi)")[0]

    def record(self):
        record()
        self.filePath = str(pathlib.Path(__file__).parent.absolute() / "record.wav")



    def improvise(self):
        if self.midiPath is None:
            QMessageBox.about(self, "No file", "No File was selected, please select a Midi file to improvise to")
        else:
            setattr(FLAGS, 'bundle_file', cfg['bundle_file2'])
            main(self.midiPath)
            if self.filePath is None:
                self.midiPath = self.midiPath.replace('midi', "improv.midi")
            else:
                self.midiPath = self.filePath + '.improv.midi'

    def bach(self):
        if self.midiPath is None:
            QMessageBox.about(self, "No file", "No File was selected, please select a Midi file to improvise to")
        else:
            setattr(FLAGS, 'bundle_file', cfg['bundle_file3'])
            main1(self.midiPath)
            if self.filePath is None:
                self.midiPath = self.midiPath.replace('midi', "bach.midi")
            else:
                self.midiPath = self.filePath + '.bach.midi'


    def melody(self):
        if self.midiPath is None:
            QMessageBox.about(self, "No file", "No File was selected, please select a Midi file to improvise to")
        else:
            setattr(FLAGS,'config', cfg['config2'])
            setattr(FLAGS, 'bundle_file',  cfg['bundle_file4'])
            main2(self.midiPath)
            if self.filePath is None:
                self.midiPath = self.midiPath.replace('midi', "melody.midi")
            else:
                self.midiPath = self.filePath + '.melody.midi'

    def chords(self):
        if self.midiPath is None:
            QMessageBox.about(self, "No file", "No File was selected, please select a Midi file to improvise to")
        else:
            setattr(FLAGS,'config', cfg['config1'])
            setattr(FLAGS, 'bundle_file', cfg['bundle_file1'])
            main3(self.midiPath)
            if self.filePath is None:
                self.midiPath = self.midiPath.replace('midi', "chords.midi")
            else:
                self.midiPath = self.filePath + '.chords.midi'

    def sheetmusic(self):
        subprocess.run([cfg['MuseScore'], self.midiPath])




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
