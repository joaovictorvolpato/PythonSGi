import numpy as np

from PyQt5.QtGui import QColor, QPainter

from typing import List

from src.Model.Drawable import Drawable
from src.Model.Point import Point

from src.Model.Utils.ViewPortTransform import viewportTransformation
from src.Model.Utils.BezierUtils import getGBBezier, blendingFunction
from src.Model.Clipping.CurveClipper import curveClip


class Bezier(Drawable):
    def __init__(
        self,coordinates: List[Point], color: QColor = None, window=None, name: str = None,
    ):
        super().__init__(name, color)

        if len(coordinates) < 4:
            print("Invalid number of points for Bezier Curve")

        if (len(coordinates) - 4) % 3 != 0:
            print("Invalid number of points for Bezier Curve")

        self.__coordinates = coordinates
        self.__original_coordinates = coordinates
        self.__window = window
        self.__curve_points = []

    @property
    def coordinates(self) -> List[Point]:
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, coordinates: List[Point]) -> None:
        self.__coordinates = coordinates

    def draw(self, painter: QPainter) -> None:
        acc = 0.001
        for i in range(0, len(self.__coordinates) - 3, 3):
            gb = getGBBezier(
                self.__coordinates[i],
                self.__coordinates[i + 1],
                self.__coordinates[i + 2],
                self.__coordinates[i + 3],
            )

            t = 0.0

            while t <= 1.0:
                x1 = blendingFunction(t, gb.x)
                y1 = blendingFunction(t, gb.y)
                x2 = blendingFunction(t + acc, gb.x)
                y2 = blendingFunction(t + acc, gb.y)

                x1, y1 = self.normalize(x1, y1)
                x2, y2 = self.normalize(x2, y2)
                x1, y1, x2, y2 = curveClip(x1, y1, x2, y2, self.__window)

                self._drawLines(x1, y1, x2, y2, painter)

                t += acc

                self.__curve_points.extend([Point(x1, y1, self.__window), Point(x2, y2, self.__window)])

    def _drawLines(self, x1, y1, x2, y2, painter):
        if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
            x1, y1 = viewportTransformation(x1, y1, self.__window)
            x2, y2 = viewportTransformation(x2, y2, self.__window)
            painter.drawLine(x1, y1, x2, y2)

    def normalize(self, x, y):
        yw_min, yw_max, xw_min, xw_max = self.__window.getMinsAndMaxes()
        normal_x = (x - xw_min) / (xw_max - xw_min) * 2 - 1
        normal_y = (y - yw_min) / (yw_max - yw_min) * 2 - 1
        return (normal_x, normal_y)

    def transform(self, matrix: np.ndarray) -> None:
        for point in self.__coordinates:
            mult = np.dot(np.array([point.x, point.y, 1]), matrix)
            point.x = mult.item(0)
            point.y = mult.item(1)

    def getCenter(self) -> list:
        sum_x = 0
        sum_y = 0
        for point in self.__coordinates:
            sum_x += point.x
            sum_y += point.y

        return [sum_x / len(self.__coordinates), sum_y / len(self.__coordinates)]

    def reset(self) -> None:
        for point in self.__coordinates:
            point.reset()

    def transformToView(self):
      pass
