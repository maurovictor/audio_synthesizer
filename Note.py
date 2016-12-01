# -*- coding: utf-8 -*-
import sys, time
import numpy as np; import sounddevice as sd
from PyQt4.QtCore import *; from PyQt4 import QtGui


class Note(QObject):

    played = pyqtSignal(float)

    def __init__(self, frequency):
        QObject.__init__(self)
        self.frequency = frequency
        self.sample_freq = 48000
        self.sample_period = 1./self.sample_freq


    def play(self):
        #Amostras por bloco, tempo 3 períodos dividido por período de amostragem
        self.samples_per_chunk = int(round((3*(1./self.frequency))/(self.sample_period)))
        self.n = np.arange(0, self.samples_per_chunk)
        self.w = 2*np.pi*self.frequency

        self.t = self.n*self.sample_period

        self.sinal = np.sin(self.w*self.t)

        sd.play(self.sinal, self.sample_freq, loop=True)

    def stop(self):
        sd.stop()
