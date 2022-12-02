import os
import sys
import time
import logging
import PyQt5
import signal
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMainWindow, QComboBox, QGridLayout, QMessageBox, QTextBrowser
# Création fenètre chrono

class EcranPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)

        # Titre fenêtre
        self.setWindowTitle("Chronomètre")

        # Création des widgets
        self.label = QLabel("Compteur :")
        self.label2 = QLineEdit("0")
        self.label2.setReadOnly(True)
        self.bouton_start = QPushButton("Start")
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.label2, 1, 0, 2, 2)
        grid.addWidget(self.bouton_start, 3, 0, 1, 2)

        self.bouton_reset = QPushButton("Reset")
        self.bouton_stop = QPushButton("Stop")
        grid.addWidget(self.bouton_reset, 4, 0, 1, 1)
        grid.addWidget(self.bouton_stop, 4, 1, 1, 1)
        self.bouton_reset.setEnabled(False)
        self.bouton_stop.setEnabled(False)
        self.bouton_connect = QPushButton("Connect")
        self.bouton_quitter = QPushButton("Quitter")
        grid.addWidget(self.bouton_connect, 5, 0, 1, 1)
        grid.addWidget(self.bouton_quitter, 5, 1, 1, 1)

        # Connexion des boutons
        self.bouton_start.clicked.connect(self.start_chrono)
        self.bouton_reset.clicked.connect(self.reset_chrono)
        self.bouton_stop.clicked.connect(self.stop_chrono)
        self.bouton_connect.clicked.connect(self.connect)
        self.bouton_quitter.clicked.connect(self.quitter)

    def quitter(self):
        client.send(b"bye")
        self.close()
    
    def start_chrono(self):
        self.label2.setText("0")
        self.bouton_start.setEnabled(False)
        self.bouton_reset.setEnabled(True)
        self.bouton_stop.setEnabled(True)
        self.timer = PyQt5.QtCore.QTimer()
        self.timer.start(1000)
        self.timer.timeout.connect(self.update)
        client.send(b"start clicked")
    
    def stop_chrono(self):
        self.timer.stop()
        self.bouton_start.setEnabled(True)
        self.bouton_reset.setEnabled(True)
        self.bouton_stop.setEnabled(False)
        self.timer.stop()
        client.send(self.label2.text().encode())
        client.send(b"stop clicked")
        
    def update(self):
        self.label2.setText(str(int(self.label2.text()) + 1))
    
    def reset_chrono(self):
        self.label2.setText("0")

    def connect(self):
        global client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect(("127.0.0.1", 10000))
            if client:
                self.bouton_connect.setEnabled(False)
                self.bouton_connect.setText("Connecté")
        except socket.error:
            QMessageBox.critical(self, "Erreur", "Impossible de se connecter au serveur")
        
        return False
        




#Fermeture en cas de CTRL C
def fermerClient():
    print("Fermeture du client")
    client.send(b"bye")
    sys.exit(0)




signal.signal(signal.SIGINT, fermerClient)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    window = EcranPrincipal()
    window.show()

    app.exec()