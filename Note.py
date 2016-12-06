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

    def __init__(self, frequency, max_value, active_time):
        QObject.__init__(self)

        self.fs = 5000
        self.Ts = 1.0 / self.fs
        self.w = 2 * np.pi * frequency

        self.samples = np.arange(0, (active_time + 1.5) * self.fs)
        self.t = (self.samples * self.Ts)

        self.declination = (0.3 - max_value) / active_time
        self.decay_envelope = (self.t * self.declination) + max_value
        self.decay_rec = rec(self.samples, 0, active_time * self.fs)
        self.release_rec = rec(self.samples, active_time * self.fs, len(self.samples))

        self.decay_signal = np.sin(self.w * self.t) * self.decay_envelope * self.decay_rec




        self.release_samples = np.arange(0, 1.5 * self.fs )
        self.release_t = self.samples * self.Ts
        self.rel_declination = (0 - 0.3) / 1.5
        self.release_envelope = (self.release_t * self.rel_declination) + 0.4
        self.release_rec = rec(self.samples, active_time * self.fs, len(self.samples))
        self.release_signal = np.sin(self.w * self.release_t) * self.release_envelope * self.release_rec

        self.signal = self.decay_signal + self.release_signal

        #sd.stop()
        #sd.play(self.signal, self.fs)
        # plt.stem(self.samples, self.decay_signal)
        # plt.figure()
        plt.stem(self.samples, self.signal)
        plt.show()



    def play(self):

        # max_point = [attack_samples, max_value]
        # sustain_point = [attack_samples + samples, sustain_value]

        # sd.play(decay)
        # sd.play(sustain) #with loop=True
        return

    def stop(self):
        sd.stop()
