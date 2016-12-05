# -*- coding: utf-8 -*-
import sys
import sounddevice
from PyQt4 import QtCore, QtGui
from math import sin, pi
from pyaudio import PyAudio


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(500, 200, 600, 500)
        self.setWindowTitle("Sinteizador de Audio")

        self.home()

    def home(self):
        #Criando os botões brancos
        
        btnDo = QtGui.QPushButton("Do", self)
        btnDo.setShortcut("d")
        btnDo.pressed.connect(self.play)
        btnDo.released.connect(self.stop)
        #btnDo.timerEvent(self)
        #btnDo.toggled.connect(self.play)
        
        btnRe = QtGui.QPushButton("Re", self)
        btnRe.setShortcut("f")
        btnRe.clicked.connect(self.play)
    
        btnMi = QtGui.QPushButton("Mi", self)
        btnMi.setShortcut("g")
        btnMi.clicked.connect(self.play)

        btnFa = QtGui.QPushButton("Fa", self)
        btnFa.setShortcut("h")
        btnFa.clicked.connect(self.play)

        btnSol = QtGui.QPushButton("Sol", self)
        btnSol.setShortcut("j")
        btnSol.clicked.connect(self.play)

        btnLa = QtGui.QPushButton("La", self)
        btnLa.setShortcut("k")
        btnLa.clicked.connect(self.play)

        btnSi = QtGui.QPushButton("Si", self)
        btnSi.setShortcut("l")
        btnSi.clicked.connect(self.play)
        
        #Criando os botões pretos
        btnDoS = QtGui.QPushButton("DoS", self)
        btnDoS.setShortcut("r")
        btnDoS.clicked.connect(self.play)
        
        btnReS = QtGui.QPushButton("ReS", self)
        btnReS.setShortcut("t")
        btnReS.clicked.connect(self.play)
        
        btnFaS = QtGui.QPushButton("FaS", self)
        btnFaS.setShortcut("u")
        btnFaS.clicked.connect(self.play)
        
        btnSolS = QtGui.QPushButton("SolS", self)
        btnSolS.setShortcut("i")
        btnSolS.clicked.connect(self.play)
        
        btnLaS = QtGui.QPushButton("LaS", self)
        btnLaS.setShortcut("o")
        btnLaS.clicked.connect(self.play)

        white_btn_list = [btnDo, btnRe, btnMi, btnFa, btnSol, btnLa, btnSi]
        black_btn_list = [btnDoS, btnReS, btnFaS, btnSolS, btnLaS]

        self.key_width = 60
        self.key_heigh = 300
        self.black_width = 20
        self.black_heigh = 120

        for i in xrange(0, len(white_btn_list)):
            #Definindo a cor, tamanho e posição das teclas brancas
            white_btn_list[i].setStyleSheet("background-color: white") 
            white_btn_list[i].resize(self.key_width, self.key_heigh)
            white_btn_list[i].move(100 + (self.key_width*i),100)


        for i in xrange(0, len(black_btn_list)):
            #Definindo a cor, tamanho e posição das teclas pretas
            black_btn_list[i].setStyleSheet("background-color: black")
            black_btn_list[i].resize(self.black_width,self.black_heigh)
            #Mover as teclas pretas de acordo com sua posição para se asemelhar ao piano
            if i<=1:
                black_btn_list[i].move(150+(60*i), 100)
            else:
                black_btn_list[i].move(210+(60*i), 100)

        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("Piano")
        comboBox.addItem("Baixo")
        comboBox.addItem("Instrumento3")
        comboBox.addItem("Instrumento4")
        comboBox.move(250, 10)

        
        self.show()

    def stop(self):
        print("stop")
        

    def play(self):
        
        sender = self.sender()
        if sender.text() == 'Do':
            self.statusBar().showMessage(sender.text() + ' was pressed')
            FreqNota = 261.63

        if sender.text() == 'DoS':
            self.statusBar().showMessage(sender.text() + ' was pressed')
            FreqNota = 277.18
            
        if sender.text() == 'Re':
            self.statusBar().showMessage(sender.text() + ' was pressed')
            FreqNota = 293.66

        if sender.text() == 'ReS':
            self.statusBar().showMessage(sender.text() + 'was pressed')
            FreqNota = 311.13

        if sender.text() == 'Mi':
            self.statusBar().showMessage(sender.text() + ' was pressed')
            FreqNota = 329.63

        if sender.text() == 'Fa':
            self.statusBar().showMessage(sender.text() + ' was pressed')
            FreqNota = 349.23

        if sender.text() == 'FaS':
            self.statusBar().showMessage(sender.text() + 'was pressed')
            FreqNota = 369.99

        if sender.text() == 'Sol':
            self.statusBar().showMessage(sender.text() + ' was pressed')
            FreqNota = 391.99

        if sender.text() == 'SolS':
            self.statusBar().showMessage(sender.text() + 'was pressed')
            FreqNota = 415.30

        if sender.text() == 'La':
            self.statusBar().showMessage(sender.text() + ' was pressed')
            FreqNota = 440

        if sender.text() == 'LaS':
            self.statusBar().showMessage(sender.text() + ' was pressed')
            FreqNota = 466.16

        if sender.text() == 'Si':
            self.statusBar().showMessage(sender.text() + ' was pressed')
            FreqNota = 493.88
            
         
        # veja http://en.wikipedia.org/wiki/Bit_rate#Audio
        TAXA = 10025           # qtde de amostras/s
        Ts = 1./TAXA            # intervalo entre amostras (período de amostragem)

        # veja http://www.phy.mtu.edu/~suits/notefreqs.html
        FREQUENCIA = FreqNota

        DURACAO = 1.            # duração da nota, em segundos
        QTD_AMOSTRAS = int(TAXA * DURACAO)
        AMOSTRAS_RESTANTES = QTD_AMOSTRAS % TAXA
        NOTA = ''               # amostras (formato ASCII) p/ serem tocadas pelo PyAudio

        for n in xrange(QTD_AMOSTRAS):
          NOTA = NOTA + chr(int(sin(2*pi*FREQUENCIA*n*Ts)*127+128))

        # preenche o restante do conjunto com silêncio
        for n in xrange(AMOSTRAS_RESTANTES):
          NOTA = NOTA + chr(128)

        p = PyAudio()           # objeto de som (saída - auto-falante)
        fluxo = p.open(format=p.get_format_from_width(1),channels=1,rate=TAXA,output=True)
        fluxo.write(NOTA)       # toca a nota criada

        #if bool(btnDo.released) == 'true':
         #   fluxo.stop_stream()     # para de tocar a nota
          #  fluxo.close()
           # p.terminate()


def run():
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())

run()
