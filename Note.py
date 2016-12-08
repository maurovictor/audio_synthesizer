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

    def __init__(self, frequency, max_value, attack_time, decay_time, release_time, oitava):
        QObject.__init__(self)

        # Definição dos parâmetros de Amostragem
        self.fs = 5000 # Frequência de amostragem
        self.Ts = 1.0 / self.fs # Período de amostragem



        # Definição da Frequência Angular
        self.w = 2 * np.pi * frequency

        # Calculando o número de amostras
        self.samples = np.arange(0, (attack_time + decay_time + release_time) * self.fs)

        # Colocando na base do Tempo
        self.t = self.samples * self.Ts


        # Criando as janelas para os intervalos de ATAQUE, DECAIMENTO e RELAXAMENTO
        self.attack_rec = rec(self.samples, 0, attack_time * self.fs)
        self.decay_rec = rec(self.samples, attack_time * self.fs, (attack_time + decay_time) * self.fs)
        self.release_rec = rec(self.samples, (attack_time + decay_time) * self.fs, (attack_time + decay_time + release_time) * self.fs)


        # Definindo os parâmetros das retas do envelope
        self.att_inclination = max_value / attack_time #Inclinação do ATAQUE
        self.att_shift = 0 # Coeficiente Linear(Deslocamento da reta)

        self.dec_inclination = (0.2 - max_value) / decay_time #Inclinação do DECAY
        self.dec_shift = max_value - (attack_time * self.dec_inclination)

        self.rel_inclination = (0 - 0.2) / release_time #Inclinação do RELEASE
        self.rel_shift = 0.2 - ((attack_time + decay_time) * self.rel_inclination)

        # Criando os envelopes
        self.attack_envelope = (self.t * self.att_inclination) + self.att_shift
        self.decay_envelope = (self.t * self.dec_inclination) + self.dec_shift
        self.release_envelope = (self.t * self.rel_inclination) + self.rel_shift


        self.attack_signal = np.sin(self.w * self.t) * self.attack_envelope * self.attack_rec
        self.decay_signal = np.sin(self.w * self.t) * self.decay_envelope * self.decay_rec
        self.release_signal = np.sin(self.w * self.t) * self.release_envelope * self.release_rec

        #Sinal pronto e modulado
        self.signal = self.attack_signal + self.decay_signal + self.release_signal





    def play(self):
        sd.stop()
        sd.play(self.signal, self.fs)
        #plt.stem(self.attack_signal)
        #plt.show()
