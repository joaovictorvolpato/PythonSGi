
from PyQt5.QtWidgets import (
     QMainWindow
)

from PyQt5 import QtCore, QtGui, QtWidgets


from src.View.main_ui import Ui_Dialog
from src.Controllers.Controller import Controller

class View(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__controller = Controller()
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.pushButton_3.clicked.connect(self.moveUp)
        self.pushButton_4.clicked.connect(self.moveRight)
        self.pushButton_5.clicked.connect(self.moveDown)
        self.pushButton_6.clicked.connect(self.moveLeft)
        self.comboBox.currentIndexChanged.connect(self.changeObjectType)
        self.pushButton.clicked.connect(self.zoomIn)
        self.pushButton_2.clicked.connect(self.zoomOut)

    def moveUp(self):
        # Implemente a lógica para mover para cima
        print('moveUp')

    def moveRight(self):
        # Implemente a lógica para mover para a direita
        print('moveRight')

    def moveDown(self):
        # Implemente a lógica para mover para baixo
        print('moveDown')

    def moveLeft(self):
        # Implemente a lógica para mover para a esquerda
        print('moveLeft')

    def changeObjectType(self, index):
        # Implemente a lógica para mudar o tipo de objeto
        print('changeObjectType')

    def zoomIn(self):
        # Implemente a lógica para dar zoom in
        print('zoomIn')

    def zoomOut(self):
        # Implemente a lógica para dar zoom out
        print('zoomOut')