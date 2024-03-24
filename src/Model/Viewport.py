from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.DisplayFile import DisplayFile
from src.Model.Patterns.observer import Observed

class Viewport(QtWidgets.QWidget, Observed):
    def __init__(self, parent=None):
        self.__currentColor = QtCore.Qt.red
        self.__displayFile = DisplayFile()
        self.clicked_x = 0
        self.clicked_y = 0 

    def mousePressEvent(self, event):
        #print("Current type: ", self.currentSelectedType)
        print("Mouse pressed at: ", event.pos().x(), event.pos().y())
        self.clicked_x = event.pos().x()
        self.clicked_y = event.pos().y()
        self.notify()
        self.update()
        
    def paintEvent(self, ev):
        qp = QtGui.QPainter(self)
        qp.setPen(self.__currentColor)
        qp.setBrush(self.__currentColor)
        qp.drawEllipse(self.x, self.y, 100, 100)

    def attach_controller(self, controller):
        self.attach(controller)
