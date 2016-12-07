# -*- coding: utf-8 -*-
import sys
import numpy as np
from signal_functions import *
import scipy.signal as sc
import sounddevice as sd
from PyQt4.QtCore import *

import matplotlib.pyplot as plt





class Note(QObject):

    played = pyqtSignal(float)

    def __init__(self, frequency, max_value, attack_time, decay_time, release_time):
        QObject.__init__(self)

        self.fs = 5000 # Frequência de amostragem
        self.Ts = 1.0 / self.fs # Período de amostragem
        self.w = 2 * np.pi * frequency # Frequência Angular

        self.samples = np.arange(0, (attack_time + decay_time + release_time) * self.fs)

        self.t = self.samples * self.Ts

        self.attack_rec = rec(self.samples, 0, attack_time * self.fs)
        self.decay_rec = rec(self.samples, attack_time * self.fs, (attack_time + decay_time) * self.fs)
        self.release_rec = rec(self.samples, (attack_time + decay_time) * self.fs, (attack_time + decay_time + release_time) * self.fs)

        self.att_inclination = max_value / attack_time
        self.att_shift = 0
        self.dec_inclination = (0.2 - max_value) / decay_time
        self.dec_shift = max_value - (attack_time * self.dec_inclination)
        self.rel_inclination = (0 - 0.2) / release_time
        self.rel_shift = 0.2 - ((attack_time + decay_time) * self.rel_inclination)

        self.attack_envelope = (self.t * self.att_inclination) + self.att_shift
        self.decay_envelope = (self.t * self.dec_inclination) + self.dec_shift
        self.release_envelope = (self.t * self.rel_inclination) + self.rel_shift

        self.attack_signal = np.sin(self.w * self.t) * self.attack_envelope * self.attack_rec
        self.decay_signal = np.sin(self.w * self.t) * self.decay_envelope * self.decay_rec
        self.release_signal = np.sin(self.w * self.t) * self.release_envelope * self.release_rec

        self.signal = self.attack_signal + self.decay_signal + self.release_signal

        #plt.stem(self.samples)
        #plt.stem(self.attack_rec)
        #plt.figure()
        #plt.stem(self.decay_rec)
        #plt.figure()
        #plt.stem(self.release_rec)
        #plt.show()





        sd.stop()
        sd.play(self.signal, self.fs)
        #plt.stem(self.attack_signal)
        #plt.figure()
        #plt.stem(self.decay_signal)
        #plt.figure()
        #plt.stem(self.release_signal)


        # plt.figure()
        #plt.stem(self.decay_envelope)
        #plt.show()



    def play(self):

        # max_point = [attack_samples, max_value]
        # sustain_point = [attack_samples + samples, sustain_value]

        # sd.play(decay)
        # sd.play(sustain) #with loop=True
        return

    def stop(self):
        sd.stop()
