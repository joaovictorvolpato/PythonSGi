from abc import ABC, abstractmethod
from Patterns.observer import Observed
from typing import Any

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

    @property
    def name(self, name:str):
        self.__name = name

    @name.setter
    def name(self):
        return self.__name
    
    @property
    def color(self, color:QtCore.Qt.GlobalColor):
        self.__color = color

    @color.setter
    def color(self):
        return self.__color