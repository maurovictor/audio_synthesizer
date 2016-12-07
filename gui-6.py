# -*- coding: utf-8 -*-
import sys
from functools import partial;
from math import sin, pi; from pyaudio import PyAudio
from PyQt4.QtCore import *
from PyQt4 import QtGui
from Note import *

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(500, 200, 600, 500)
        self.setWindowTitle("Sinteizador de Audio")
        self.setWindowIcon(QtGui.QIcon('Icon.png'))
        self.setFixedSize(600, 500)
        self.home()

    def home(self):
        self.nameNotes = ["Do", "Re", "Mi", "Fa", "Sol", "La", "Si"]
        self.nameNotesS = ["DoS", "ReS", "FaS", "SolS", "LaS"]

        self.whiteFreq = [261.63, 293.66, 329.63, 349.23, 391.99, 440.0, 493.88]
        self.blackFreq = [277.18, 311.13, 369.99, 415.3, 466.16]


        self.whiteShortcuts = ['d','f', 'g','h','j','k','l']
        self.blackShortcuts = ['r','t', 'u','i','o']


        self.bntsWhite = []
        self.bntsBlack = []
        self.whiteWidth = 60
        self.whiteHeigh = 300
        self.blackWidth = 20
        self.blackHeigh = 120


        #Criando e configurando os botões brancos
        for index, value in enumerate(self.whiteFreq):
            key = self.bntsWhite
            key.append(QtGui.QPushButton(str(self.nameNotes[index]),self))
            key[index].setShortcut(self.whiteShortcuts[index])
            key[index].setStyleSheet("background-color: white")
            key[index].resize(self.whiteWidth, self.whiteHeigh)
            key[index].move(100 + (self.whiteWidth*index),100)
            key[index].clicked.connect(partial(on_press,
                                               float(self.whiteFreq[index])))

        #Criando e configurando os botões pretos
        for index, value in enumerate(self.blackFreq):
            key = self.bntsBlack
            key.append(QtGui.QPushButton(str(self.nameNotesS[index]), self))
            key[index].setShortcut(self.blackShortcuts[index])
            key[index].setStyleSheet("background-color: black; color: black")
            key[index].resize(self.blackWidth,self.blackHeigh)
            key[index].clicked.connect(partial(on_press,
                                               float(self.blackFreq[index])))
            if index<=1:
                key[-1].move(150+(60*index), 100)
            else:
                key[-1].move(210+(60*index), 100)



        #Botões de alterações de oitavas
        bntOctavesL = QtGui.QPushButton("<",self)
        bntOctavesL.clicked.connect(self.diminuir)
        bntOctavesL.setShortcut("<")
        bntOctavesL.resize(50,50)
        bntOctavesL.move(100+7*60-100, 50)

        bntOctavesH = QtGui.QPushButton(">",self)
        bntOctavesH.clicked.connect(self.aumentar)
        bntOctavesH.setShortcut(">")
        bntOctavesH.resize(50,50)
        bntOctavesH.move(100+7*60-50, 50)

        self.show()


    def FrequenceNoteW(self, FreqNote):
        global whiteFreq
        sender = self.sender()

        self.FreqNote = [0, 0, 0, 0, 0, 0, 0]

        for index, value in enumerate(self.whiteFreq):
            self.FreqNote[index] = self.whiteFreq[index]

        if sender.text() == 'Do':
            self.play(float(self.FreqNote[0]))
        if sender.text() == 'Re':
            self.play(float(self.FreqNote[1]))
        if sender.text() == 'Mi':
            self.play(float(self.FreqNote[2]))
        if sender.text() == 'Fa':
            self.play(float(self.FreqNote[3]))
        if sender.text() == 'Sol':
            self.play(float(self.FreqNote[4]))
        if sender.text() == 'La':
            self.play(float(self.FreqNote[5]))
        if sender.text() == 'Si':
            self.play(float(self.FreqNote[6]))


    def FrequenceNoteB(self, FreqNote):
        global blackFreq

        sender = self.sender()

        self.FreqNote = [0, 0, 0, 0, 0]

        for index, value in enumerate(self.blackFreq):
            self.FreqNote[index] = self.blackFreq[index]

        if sender.text() == 'DoS':
            self.play(float(self.FreqNote[0]))
        if sender.text() == 'ReS':
            self.play(float(self.FreqNote[1]))
        if sender.text() == 'FaS':
            self.play(float(self.FreqNote[2]))
        if sender.text() == 'SolS':
            self.play(float(self.FreqNote[3]))
        if sender.text() == 'LaS':
            self.play(float(self.FreqNote[4]))



    def diminuir(self):
        sender = self.sender()
        global whiteFreq

        #Diminuir Oitavas Teclas Brancas
        self.newFreqW = self.whiteFreq
        if self.whiteFreq[1] > 130:
            for index, value in enumerate(self.whiteFreq):
                self.newFreqW[index] = (self.newFreqW[index])/2
                self.whiteFreq[index] = round(self.newFreqW[index],2)

        if 600 > self.whiteFreq[1] > 520:
            self.statusBar().showMessage("Oitavas = +1")
        if 520 > self.whiteFreq[1] > 262:
            self.statusBar().showMessage("Oitava Central")
        if 262 > self.whiteFreq[1] > 130:
            self.statusBar().showMessage("Oitavas = -1")
        if 100 > self.whiteFreq[1] > 65:
            self.statusBar().showMessage("Oitavas = -2")


        #Diminuir Oitavas Teclas Pretas
        self.newFreqB = self.blackFreq
        if self.blackFreq[1] > 130:
            for index, value in enumerate(self.blackFreq):
                self.newFreqB[index] = (self.newFreqB[index])/2
                self.blackFreq[index] = round(self.newFreqB[index],2)



    def aumentar(self):

        #Aumentar Oitavas Teclas Brancas
        self.newFreq = self.whiteFreq
        if self.whiteFreq[1] < 1047:
            for index, value in enumerate(self.whiteFreq):
                self.newFreq[index] = (self.newFreq[index])*2
                self.whiteFreq[index] = round(self.newFreq[index],2)

        if 2000 > self.whiteFreq[1] > 1000:
            self.statusBar().showMessage("Oitavas = +2")
        if 600 > self.whiteFreq[1] > 520:
            self.statusBar().showMessage("Oitavas = +1")
        if 520 > self.whiteFreq[1] > 262:
            self.statusBar().showMessage("Oitava Central")
        if 262 > self.whiteFreq[1] > 130:
            self.statusBar().showMessage("Oitavas = -1")

        #Aumentar Oitavas Teclas Pretas
        self.newFreqB = self.blackFreq
        if self.blackFreq[1] < 1047:
            for index, value in enumerate(self.blackFreq):
                self.newFreqB[index] = (self.newFreqB[index])*2
                self.blackFreq[index] = round(self.newFreqB[index],2)

@pyqtSlot(float)
def on_press(freq):
    note = Note(freq, 1, .001, .5, .7)
    note.play()



@pyqtSlot()
def on_release():
    sd.stop()


def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()




def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
