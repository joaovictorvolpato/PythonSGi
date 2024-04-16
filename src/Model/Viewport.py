from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.DisplayFile import DisplayFile
from src.Model.Clipper import Clipper
from src.Model.Patterns.observer import Observed
from src.Model.Line import Line

class Viewport(QtWidgets.QWidget, Observed):
    def __init__(self, parent=None):
        super(QtWidgets.QWidget,self).__init__(parent)
        self.__currentColor = QtCore.Qt.red
        self.__displayFile = DisplayFile()
        self.__clipper = Clipper()
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
        #print("Painting viewport")
        qp = QtGui.QPainter(self)
        qp.setRenderHint(QtGui.QPainter.Antialiasing)

        brush = QtGui.QBrush(self.__currentColor)
        brush.setStyle(QtCore.Qt.SolidPattern)
        qp.setPen(self.__currentColor)
        qp.setBrush(brush)

        self.__clipper.line_clipper = self.displayFile.selected_clipping_algorithm
        objects_to_draw = self.__clipper.clip(self.displayFile)

        print(objects_to_draw)

        for obj in objects_to_draw:
            #if not isinstance(obj, Line):
                #print(obj.window.x_min, obj.window.y_min, obj.window.x_max, obj.window.y_max)              
            if obj is self.displayFile.get_buffer():
                pen = QtGui.QPen(self.__currentColor, 3)
                qp.setPen(pen)
            else:
                color = obj.color if obj.color is not None else QtCore.Qt.GlobalColor.black

                pen = QtGui.QPen(color, 3)
                qp.setPen(pen)
                brush = QtGui.QBrush(color)
                qp.setBrush(brush)
            print("Drawing object")
            obj.draw(qp)

        _buffer = self.displayFile.get_buffer()
        if _buffer is None:
            return
        
        pen = QtGui.QPen(self.__currentColor, 3)
        qp.setPen(pen)
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
