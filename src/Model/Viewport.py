from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.DisplayFile import DisplayFile
from src.Model.Patterns.observer import Observed

class Viewport(QtWidgets.QWidget, Observed):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget,self).__init__(parent)
        self.__currentColor = QtCore.Qt.red
        self.__displayFile = DisplayFile()
        self.__clicked_x = 0
        self.__clicked_y = 0

    def mousePressEvent(self, event):
        #print("Current type: ", self.currentSelectedType)
        print("Mouse pressed at: ", event.pos().x(), event.pos().y())
        self.__clicked_x = event.pos().x()
        self.__clicked_y = event.pos().y()
        print("Clicked at: ", self.__clicked_x, self.__clicked_y)
        self.notify()
        #self.update()

    def paintEvent(self, ev):
        print("Painting viewport")
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        brush = QtGui.QBrush(self.__currentColor)
        brush.setStyle(QtCore.Qt.SolidPattern)
        qp.setPen(self.__currentColor)
        qp.setBrush(brush)

        for point in self.displayFile.points:
            normal_x, normal_y = self.displayFile.normalizeObject(point)
            point.setNormalCoordinates(normal_x, normal_y)

        for line in self.displayFile.lines:
            for point in line.points:
                normal_x, normal_y = self.displayFile.normalizeObject(point)
                point.setNormalCoordinates(normal_x, normal_y)

        for wireframe in self.displayFile.wireframes:
            for point in wireframe.points:
                normal_x, normal_y = self.displayFile.normalizeObject(point)
                point.setNormalCoordinates(normal_x, normal_y)

        for obj in self.displayFile.getObjects():
            if obj is self.displayFile.get_buffer():
                pen = QtGui.QPen(self.__currentColor, 3)
                qp.setPen(pen)
            else:
                color = obj.color
                pen = QtGui.QPen(color, 3)
                qp.setPen(pen)
                brush = QtGui.QBrush(color)
                qp.setBrush(brush)
            print("Drawing object")
            obj.draw(qp)

    @property
    def clicked_x(self):
        return self.__clicked_x

    @property
    def clicked_y(self):
        return self.__clicked_y

    @property
    def displayFile(self):
        return self.__displayFile

    def attach_controller(self, controller):
        self.attach(controller)
