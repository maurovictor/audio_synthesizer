# -*- coding: utf-8 -*-
import sys
import numpy as np
import sounddevice as sd
from PyQt4.QtCore import *

import matplotlib.pyplot as plt





class Note(QObject):

    played = pyqtSignal(float)

    def __init__(self, frequency, attack_samples, decay_samples, max_value, sustain_value=0):
        QObject.__init__(self)

        self.fs = 50000
        self.Ts = 1.0 / self.fs

        self.w = 2 * np.pi * frequency
        self.samples_per_chunk = int(round((3 * (1.0 / frequency)) / (self.Ts)))
        self.n = np.arange(0, self.samples_per_chunk + 1)
        self.t = self.Ts * self.n
        self.signal = np.sin(self.w * self.t)


        self.inclination = (sustain_value - max_value) / decay_samples
        self.vertical_shift = max_value - (self.inclination * attack_samples)
        self.decay_samples = np.arange(0, decay_samples + 1)
        self.decay_t = self.decay_samples * self.Ts
        self.decay_envelope = (self.inclination * self.decay_samples + self.vertical_shift) * self.Ts

        self.decay_signal = np.sin(self.w * self.decay_t) * self.decay_envelope

        sd.play(self.decay_signal, self.fs)


    def play(self):

        # max_point = [attack_samples, max_value]
        # sustain_point = [attack_samples + decay_samples, sustain_value]

        # sd.play(decay)
        # sd.play(sustain) #with loop=True
        return

    def stop(self):
        sd.stop()
