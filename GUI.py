#This script is the PyQt5 implementation
import WaveToMidiTranscription
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QInputDialog, QLineEdit, QTextEdit #GUI with PyQt5
import sys
app = QApplication(sys.argv)
win=QMainWindow()
win.setGeometry(80,100,600,600)
win.setWindowTitle('Wave to Midi Transcription!')

label = QtWidgets.QLabel(win)
label.setText("My First Label")


button= QPushButton("Click me")

win.show()
sys.exit(app.exec_())