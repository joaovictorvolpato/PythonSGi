from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.DisplayFile import DisplayFile
from src.Model.Clipper import Clipper
from src.Model.Patterns.observer import Observed
class Viewport(QtWidgets.QWidget, Observed):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget,self).__init__(parent)
        self.__currentColor = QtCore.Qt.red
        self.__displayFile = DisplayFile()
        self.__clipper = Clipper()
        self.__clicked_x = 0
        self.__clicked_y = 0

    def mousePressEvent(self, event):
        self.__clicked_x = event.pos().x()
        self.__clicked_y = event.pos().y()
        self.notify()

    def paintEvent(self, ev):
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        brush = QtGui.QBrush(self.__currentColor)
        brush.setStyle(QtCore.Qt.SolidPattern)
        qp.setPen(self.__currentColor)
        qp.setBrush(brush)

        #self.__clipper.line_clipper = self.displayFile.selected_clipping_algorithm
        objects_to_draw = self.__clipper.clip(self.displayFile)

        print("OBJECTS TO DRAW", objects_to_draw[0])

        for obj in objects_to_draw:
            if obj is self.displayFile.get_buffer():
                pen = QtGui.QPen(self.__currentColor, 3)
                qp.setPen(pen)
            else:
                color = obj.color if obj.color is not None else QtCore.Qt.GlobalColor.black

                pen = QtGui.QPen(color, 3)
                qp.setPen(pen)
                brush = QtGui.QBrush(color)
                qp.setBrush(brush)
            print("Drawing object", obj)
            obj.draw(qp)

        _buffer = self.displayFile.get_buffer()
        if _buffer is None:
            return

        pen = QtGui.QPen(self.__currentColor, 3)
        qp.setPen(pen)
        if isinstance(_buffer, list):
            for obj in _buffer:
                obj.draw(qp)
        else:
            _buffer.draw(qp)

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
