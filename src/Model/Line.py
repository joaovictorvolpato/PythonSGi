from src.Model.Drawable import Drawable
from src.Model.Point import Point
from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.Utils.ViewPortTransform import viewportTransformation
import numpy as np

from src.Model.Patterns.observer import Observed

class Line(Drawable, Observed):
    def __init__(self, start:Point, end:Point = None, name:str = None, window = None, color:QtCore.Qt.GlobalColor = None) -> None:
        super().__init__(name, color)
        self.__start = start
        self.__end = end
        self.__window = window

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, start:Point):
        self.__start = start

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, end:Point):
        self.__end = end

    def draw(self, painter: QtGui.QPainter,)-> None:
        start_point_x, start_point_y = viewportTransformation(
                self.start.x, self.start.y, self.__window
            )
        end_point_x, end_point_y = viewportTransformation(
                self.end.x, self.end.y, self.__window
            )
        
        #print points before and after tranformation
        print("BEFORE TRANSFORMING",self.start.x, self.start.y, self.end.x, self.end.y)
        print("AFTER TRANSFORMING",start_point_x, start_point_y, end_point_x, end_point_y)

        painter.drawLine(start_point_x, start_point_y, end_point_x, end_point_y)

    def transform(self, matrix: np.ndarray):
        start = np.dot(np.array([self.__start.x, self.__start.y, 1]), matrix)
        end = np.dot(np.array([self.__end.x, self.__end.y, 1]), matrix)
        self.__start.x = start.item(0)
        self.__start.y = start.item(1)
        self.__end.x = end.item(0)
        self.__end.y = end.item(1)

    def getCenter(self):
        x = (self.__start.x + self.__end.x) / 2
        y = (self.__start.y + self.__end.y) / 2
        return Point(x, y)

    def transformToView(self):
        pass 