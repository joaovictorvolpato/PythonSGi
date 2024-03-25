from abc import ABC, abstractmethod
from src.Model.Patterns.observer import Observed
from typing import Any
import numpy as np

from PyQt5 import QtCore

class Drawable(ABC):
    def __init__(self, name:str = None) -> None:
        self.__name = name
        self.__color = QtCore.Qt.black

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def transformToView(self):
        pass

    @abstractmethod
    def transform(self, matrix:np.matrix):
        pass

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def color(self, color:QtCore.Qt.GlobalColor):
        self.__color = color

    @color.setter
    def color(self):
        return self.__color