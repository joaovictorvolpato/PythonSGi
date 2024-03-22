from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog

class Viewport(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Viewport, self).__init__(parent)
        self.__currentColor = QtCore.Qt.red
        self.x = 0
        self.y = 0
        self.currentSelectedType = ""
        self.currentClippingMethod = ""

    def mousePressEvent(self, event):
        #print("Current type: ", self.currentSelectedType)
        print("Mouse pressed at: ", event.pos().x(), event.pos().y())
        self.x = event.pos().x()
        self.y = event.pos().y()
        self.update()
        

    def paintEvent(self, ev):
        qp = QtGui.QPainter(self)
        qp.setPen(self.__currentColor)
        qp.setBrush(self.__currentColor)
        qp.drawEllipse(self.x, self.y, 100, 100)