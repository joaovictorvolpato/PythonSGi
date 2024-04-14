from src.Model.Drawable import Drawable
from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.Patterns.observer import Observed
from src.Model.Window import Window
from src.Model.Utils.ViewPortTransform import viewportTransformation
import numpy as np

class Point(Drawable):
    def __init__(self, x:int, y:int, window:Window, name:str = None, color:QtCore.Qt.GlobalColor = None) -> None:
        super().__init__(name, color)
        self.__x = x
        self.__y = y
        self.__window = window
        self.__x_normalized = x
        self.__y_normalized = y

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
    def x_normalized(self):
        return self.__x_normalized
    
    @property
    def window(self):
        return self.__window
    
    @x_normalized.setter
    def x_normalized(self, x:int):
        self.__x_normalized = x

    @property
    def y_normalized(self):
        return self.__y_normalized
    
    @y_normalized.setter
    def y_normalized(self, y:int):
        self.__y_normalized = y

    def setNormalCoordinates(self, value_x: float, value_y: float) -> None:
        self.__x_normalized = value_x
        self.__y_normalized = value_y

    def draw(self, painter: QtGui.QPainter) -> None:
        self.normalizePoint()
        x, y = viewportTransformation(
            self.__x_normalized, self.__y_normalized, self.__window
        )
        painter.drawEllipse(x, y, 5, 5)

    def normalizePoint(self):
        print("NORMALIZED POINT", self.__x_normalized, self.__y_normalized)
        yw_min, yw_max, xw_min, xw_max = self.__window.getMinsAndMaxes()
        self.__x_normalized = (self.x - xw_min) / (xw_max - xw_min) * 2 - 1
        self.__y_normalized = (self.y - yw_min) / (yw_max - yw_min) * 2 - 1
        

    def transform(self, matrix: np.ndarray):
        mult = np.dot(np.array([self.__x, self.__y, 1]), matrix)
        self.__x = mult.item(0)
        self.__y = mult.item(1)

    def getCenter(self):
        return self

    def transformToView(self):
        pass

    def getPointAsVector(self) -> str:
            return f"v {self.__x} {self.__y} 0.0"