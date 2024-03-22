from src.Model.Drawable import Drawable
from PyQt5 import QtCore
from src.Model.Patterns.observer import Observed
import numpy as np

class Point(Drawable):
    def __init__(self, x:int, y:int, name:str = None, controller:str = None) -> None:
        super().__init__(name)
        self.__x = x
        self.__y = y

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

    def draw(self):
        pass

    def transform(self, matrix: np.matrix):
        return super().transform(matrix)

    def transformToView(self):
        pass