# -*- coding: utf-8 -*-
import sys
from Note import *
from functools import partial
import matplotlib.pyplot as plt
from PyQt4.QtCore import *
from PyQt4 import QtGui


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(500, 200, 600, 500)
        self.setFixedSize(600, 500)
        self.setWindowTitle("Sintetizador de Audio")

        self.home()

    def home(self):

        self.natural_frequencies = [261.63,
                                    293.66,
                                    329.63,
                                    349.23,
                                    391.99,
                                    440.0,
                                    493.88]

        self.black_frequencies = [277.18, 311.13, 369.99, 415.3, 466.16]

        self.white_shortcuts = ['a', 's', 'd', 'f', 'g', 'h', 'j']
        self.black_shortcuts = ['w', 'e', 't', 'y', 'u']

        self.white_btns = []
        self.black_btns = []
        self.key_width = 60
        self.key_heigh = 300
        self.black_width = 20
        self.black_heigh = 120

        #Criando e configurando os botões brancos
        for i in xrange(0, len(self.natural_frequencies)):
            self.white_btns.append(QtGui.QPushButton(str(self.natural_frequencies[i]), self))
            self.white_btns[-1].setShortcut(self.white_shortcuts[i])
            self.white_btns[-1].setStyleSheet("background-color: white")
            self.white_btns[-1].resize(self.key_width, self.key_heigh)
            self.white_btns[-1].move(100 + (self.key_width * i), 100)
            self.white_btns[-1].clicked.connect(partial(on_press, float(self.natural_frequencies[i])))
            #self.white_btns[-1].pressed.connect(partial(on_press, float(self.natural_frequencies[i])))
            #self.white_btns[-1].released.connect(on_release)

        for i in xrange(0, len(self.black_frequencies)):
            self.black_btns.append(QtGui.QPushButton("", self))
            self.black_btns[-1].setStyleSheet("background-color: black")
            self.black_btns[-1].resize(self.black_width, self.black_heigh)
            if i <= 1:
                self.black_btns[-1].move(150 + (60 * i), 100)
            else:
                self.black_btns[-1].move(210 + (60 * i), 100)

            self.black_btns[-1].pressed.connect(partial(on_press, float(self.black_frequencies[i])))
            self.black_btns[-1].released.connect(on_release)

        self.show()


@pyqtSlot(float)
def on_press(freq):
    note = Note(freq, 1, .5)
    #note.play()


@pyqtSlot()
def on_release():
    sd.stop()


def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
