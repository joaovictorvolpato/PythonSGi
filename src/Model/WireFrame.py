from PyQt5 import QtGui
import numpy as np
from PyQt5.QtCore import QPoint
from PyQt5 import QtCore

from typing import List

from src.Model.Drawable import Drawable
from src.Model.Line import Line, Line3D
from src.Model.Point import Point
from src.Model.Point3D import Point3D
from src.Model.MatrixOperations import MatrixOperations3D
from src.Model.Utils.ViewPortTransform import viewportTransformation


class Wireframe(Drawable):
    def __init__(
        self, pointA: Point = None, name: str = None, window=None, color:QtCore.Qt.GlobalColor = None, is_filled: bool = False, points: list = []
    ):
        super().__init__(name,color)
        self.__firstPoint = pointA
        self.__pointsList = [pointA]
        self.__window = window
        self.__is_filled = is_filled


    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, new_window):
        self.__window = new_window

    @property
    def points(self):
        return self.__pointsList

    @points.setter
    def points(self, new_points):
        self.__pointsList = new_points

    @property
    def is_filled(self):
        return self.__is_filled

    @is_filled.setter
    def is_filled(self, new_status):
        self.__is_filled = new_status

    def draw(self, painter: QtGui.QPainter):
        if self.__is_filled:
            points = []
            for point in self.__pointsList:
                point.normalizePoint()
                x, y = viewportTransformation(point.x_normalized, point.y_normalized, self.__window)
                points.append(QPoint(x, y))
            # painter.setPen(self.__color)
            painter.drawPolygon(points)

        if len(self.__pointsList) > 1:
            for i in range(len(self.__pointsList)):
                if i == len(self.__pointsList) - 1:
                    line = Line(
                        self.__pointsList[i], self.__firstPoint, window=self.__window
                    )
                else:
                    line = Line(
                        self.__pointsList[i],
                        self.__pointsList[i + 1],
                        window=self.__window,
                    )
                line.draw(painter)
        else:
            print("obj:", self.__firstPoint)
            self.__firstPoint.draw(painter)

    def calculateGeometricCenter(self) -> list:
        xSum = 0
        ySum = 0
        for point in self.__pointsList:
            xSum += point.x
            ySum += point.y

        return [xSum / len(self.__pointsList), ySum / len(self.__pointsList)]

    def reset(self) -> None:
        for point in self.__pointsList:
            point.reset()

    def addPoint(self, point: Point):
        self.__pointsList.append(point)

    def fill(self):
        self.__is_filled = not self.__is_filled

    def transformToView(self):
        pass

    def getCenter(self):
        return self.calculateGeometricCenter()

    def transform(self, matrix: np.ndarray):
        for point in self.__pointsList:
            point.transform(matrix)

class WireFrame3D(Wireframe):
    def __init__(self, vertices: List[Point3D], faces, name: str = None, window=None):
        super().__init__(name = name)
        self.__vertices = vertices
        self.__edges = []
        self.__faces = faces
        self.__window = window

        for face in self.__faces:
            self.buildEdges([self.__vertices[x-1] for x in face])

        t = tuple(x - y for x, y in zip(self.__window.getCenter3D(), self.getCenter()))
        self.transform(MatrixOperations3D.build_translation_matrix(float(t[0]), float(t[1]), float(t[2])))

    def draw(self, painter: QtGui.QPainter):
        print("Drawing wireframe")
        for edge in self.__edges:
            edge.draw(painter)

    def buildEdges(self, coordinates):
        for point in range(len(coordinates)):
            if (not point == (len(coordinates)-1)):
                p1 = coordinates[point]
                p2 = coordinates[point + 1]
                line = Line3D(p1, p2, window=self.__window)
                self.__edges.append(line)
            else:
                p1 = coordinates[-1]
                p2 = coordinates[0]
                line = Line3D(p1, p2, window=self.__window)
                self.__edges.append(line)

    def getCenter(self):
        x_sum, y_sum, z_sum = 0, 0, 0
        for point in self.__vertices:
            x_sum += point.x
            y_sum += point.y
            z_sum += point.z

        return (x_sum / len(self.__vertices), y_sum / len(self.__vertices), z_sum/len(self.__vertices))

    def transform(self, matrix: np.ndarray):
        for point in self.__vertices:
            point.transform(matrix)