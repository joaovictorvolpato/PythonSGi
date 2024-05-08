from src.Model.Drawable import Drawable
from src.Model.Point import Point
from src.Model.Point3D import Point3D
from PyQt5 import QtCore, QtGui, QtWidgets
from src.Model.Utils.ViewPortTransform import viewportTransformation
import numpy as np

class Line(Drawable):
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

    @property
    def points(self):
        return [self.__start, self.__end]

    def draw(self, painter: QtGui.QPainter,)-> None:
        self.start.normalizePoint()
        if self.end is not None:
            self.end.normalizePoint()
        start_point_x, start_point_y = viewportTransformation(
                self.start.x_normalized, self.start.y_normalized, self.__window
            )
        end_point_x, end_point_y = viewportTransformation(
                self.end.x_normalized, self.end.y_normalized, self.__window
            )
        
        #print points before and after tranformation
        #print("BEFORE TRANSFORMING",self.start.x, self.start.y, self.end.x, self.end.y)
        #print("AFTER TRANSFORMING",start_point_x, start_point_y, end_point_x, end_point_y)

        print("Drawing line from", start_point_x, start_point_y, "to", end_point_x, end_point_y)

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
    
    def setNormalCoordinates(self, pointA: Point, pointB: Point) -> None:
        self.__start = pointA
        self.__end = pointB

    def transformToView(self):
        pass 

class Line3D(Line):
    def __init__(self, start:Point3D, end:Point3D = None, name:str = None, window = None, color:QtCore.Qt.GlobalColor = None) -> None:
        super().__init__(start, end, name, window, color)
        self.__start = start
        self.__end = end
        self.__window = window

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, start:Point3D):
        self.__start = start

    @property
    def end(self):
        return self.__end

    @end.setter
    def end(self, end:Point3D):
        self.__end = end

    @property
    def points(self):
        return [self.__start, self.__end]

    def applyTransformations(self, matrix) -> None:
        mult = np.matmul(
            np.array(
                [self.start.x, self.start.y, self.start.z, 1]
            ),
            matrix,
        )
        self.start.x = mult.item(0)
        self.start.y = mult.item(1)
        self.start.z = mult.item(2)
        mult = np.matmul(
            np.array(
                [self.end.x, self.end.y, self.end.z, 1]
            ),
            matrix,
        )
        self.end.x = mult.item(0)
        self.end.y = mult.item(1)
        self.end.z = mult.item(2)

    def getCenter(self) -> list:
        somaX = (self.start.getX() + self.end.getX()) / 2
        somaY = (self.start.getY() + self.end.getY()) / 2
        somaZ = (self.start.getZ() + self.end.getZ()) / 2

        return [somaX, somaY, somaZ]
