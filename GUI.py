import sys
import subprocess
from WaveToMidiTranscription import run
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QPushButton,QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore
from magenta.models.onsets_frames_transcription import configs
from magenta.models.onsets_frames_transcription import data
from pathlib import Path

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

        self.button1 = QPushButton('Transcribe', self)
        self.button1.setToolTip('Transcribe the wav data')
        self.button1.move(100,70)
        self.button1.clicked.connect(self.execute)
        self.button2= QPushButton('Select File to transcribe', self)
        self.button2.setToolTip('Selet the file that you want to transcribe.')
        self.button2.move(300,70)
        self.button2.clicked.connect(self.selectFile)

        self.show()

    def execute(self):
        if self.filePath is None:
            QMessageBox.about(self,'No File',"No File was selected, please select a file to transcribe")
        else:
            run(['', self.filePath], config_map=configs.CONFIG_MAP, data_fn=data.provide_batch)
            self.midiPath = self.filePath + '.midi'

    def selectFile(self):
        self.filePath = QFileDialog.getOpenFileName(self, "Choose .wav file to transcribe", "", "Wave Files (*.wav)")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())