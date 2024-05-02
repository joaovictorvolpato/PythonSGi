from src.Model.Drawable import Drawable
from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.Patterns.observer import Observed
from src.Model.Window import Window
from src.Model.Projector import Projector
from src.Model.Utils.ViewPortTransform import viewportTransformation
import numpy as np

class Point3D(Drawable):
    def __init__(self, x:int, y:int, z:int , window:Window, name:str = None, color:QtCore.Qt.GlobalColor = None) -> None:
        super().__init__(name, color)
        self.__x = x
        self.__y = y
        self.__z = z
        self.__window = window
        self.__x_normalized = x
        self.__y_normalized = y
        self.__z_normalized = z

    @property
    def x(self):
        return self.__x
    
    @x.setter
    def x(self, x:int):
        self.__x = x

    @property
    def y(self):
        return self.__y
    
    @y.setter
    def y(self, y:int):
        self.__y = y

    @property
    def z(self):
        return self.__z
    
    @z.setter
    def z(self, z:int):
        self.__z = z

    @property
    def x_normalized(self):
        return self.__x_normalized
    
    @property
    def y_normalized(self):
        return self.__y_normalized
    
    @property
    def z_normalized(self):
        return self.__z_normalized
    
    @property
    def window(self):
        return self.__window
    
    @x_normalized.setter
    def x_normalized(self, x:int):
        self.__x_normalized = x

    @y_normalized.setter
    def y_normalized(self, y:int):
        self.__y_normalized = y

    @z_normalized.setter
    def z_normalized(self, z:int):
        self.__z_normalized = z

    def setNormalCoordinates(self, value_x: float, value_y: float, value_z: float) -> None:
        self.__x_normalized = value_x
        self.__y_normalized = value_y
        self.__z_normalized = value_z

    def draw(self, painter: QtGui.QPainter, projector: Projector) -> None:
        self.normalizePoint()
        px, py = projector.project(self, self.__window)
        p = Point3D(px, py, 0, self.__window)
        p.normalizePoint()
        x, y = viewportTransformation(
            p.__x_normalized, p.__y_normalized, self.__window
        )
        painter.drawEllipse(x, y, 5, 5)

    def normalizePoint(self):
        yw_min, yw_max, xw_min, xw_max = self.__window.getMinsAndMaxes()
        self.__x_normalized = (self.x - xw_min) / (xw_max - xw_min) * 2 - 1
        self.__y_normalized = (self.y - yw_min) / (yw_max - yw_min) * 2 - 1
        #self.__z_normalized = (self.z - yw_min) / (yw_max - yw_min) * 2 - 1

    def applyTransformation(self, matrix: list) -> None:
        mult = np.matmul(np.array([self.x, self.y, self.z, 1]), matrix)
        self.x = mult.item(0)
        self.y = mult.item(1)
        self.z = mult.item(2)
        self.normalizePoint()
