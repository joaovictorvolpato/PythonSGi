from src.Model.Drawable import Drawable
from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.Patterns.observer import Observed
from src.Model.Window import Window
from src.Model.Utils.ViewPortTransform import viewportTransformation
import numpy as np

class Point(Drawable):
    def __init__(self, x:int, y:int, name:str = None, window:Window = None) -> None:
        super().__init__(name)
        self.__x = x
        self.__y = y
        self.__window = window

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

    def draw(self, painter: QtGui.QPainter) -> None:
        x, y = viewportTransformation(
            self.x, self.y, self.__window
        )
        painter.drawEllipse(x, y, 5, 5)

    def transform(self, matrix: np.matrix):
        return super().transform(matrix)

    def transformToView(self):
        pass