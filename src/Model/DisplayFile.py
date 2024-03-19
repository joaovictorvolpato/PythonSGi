from Window import Window
from Point import Point
from Line import Line

from typing import List


class DisplayFile:
    def __init__(self):
        self.__points = List[Point]
        self.__lines = List[Line]
        self.__wireframes = []
        self.__curves = []
        self.__buffer = None

        self.__window = Window()

    @property
    def points(self):
        return self.__points
    
    @property
    def lines(self):
        return self.__lines
    
    @property
    def wireframes(self):
        return self.__wireframes
    
    @property
    def curves(self):
        return self.__curves