from PyQt5.QtGui import QColor, QPainter
import numpy as np

from typing import List

from src.Model.Drawable import Drawable
from src.Model.Point import Point
from src.Model.Clipping.CurveClipper import curveClip
from src.Model.Utils.ViewPortTransform import viewportTransformation

import numpy as np

class BSplineGeoMatrix:
    def __init__(self, x: List[List[float]], y: List[List[float]]):
        self.x = x
        self.y = y

class BSpline(Drawable):

    def __init__(
        self, first_control_point: Point, name: str = None, color: QColor = None, window=None
    ):
        super().__init__(name)

        self.BSPLINE_MATRIX = [
            [-1 / 6, 1 / 2, -1 / 2, 1 / 6],
            [1 / 2, -1, 1 / 2, 0],
            [-1 / 2, 0, 1 / 2, 0],
            [1 / 6, 2 / 3, 1 / 6, 0],
            ]

        self.__control_points = [first_control_point]
        self.__window = window

        for point in self.__control_points:
            point.normalizePoint()

        if color == None:
            self.__color = QColor(0, 0, 0)
        else:
            self.__color = color

    def addControlPoint(self, point: Point) -> None:
        point.normalizePoint()
        self.__control_points.append(point)

    def draw(self, painter: QPainter) -> None:
        delta = 0.001
        n = 1 / delta
        delta_matrix = self.calculateDeltaMatrix(delta)

        print("printing delta matrix", delta_matrix)

        #print(len(self.__control_points))

        for i in range(len(self.__control_points) - 3):
            #print("getting points", i, i + 1, i + 2, i + 3)
            #print(self.__control_points[i], self.__control_points[i + 1], self.__control_points[i + 2], self.__control_points[i + 3])

            gb_spline = self.getGBSpline(
                self.__control_points[i],
                self.__control_points[i + 1],
                self.__control_points[i + 2],
                self.__control_points[i + 3],
            )

            dx, dy = self.getInitialCurve(delta_matrix, gb_spline)

            #print("initial curve:", dx, dy)

            for point in self.__control_points:
                point.draw(painter)

            #print("Called Forward Differences")
        
            self.forward_difference(n, dx, dy, self.__window, painter=painter)


    def calculateDeltaMatrix(self, delta: float) -> np.array:
        delta2 = delta**2
        delta3 = delta2 * delta

        return np.array(
            [
                [0, 0, 0, 1],
                [delta3, delta2, delta, 0],
                [6 * delta3, 2 * delta2, 0, 0],
                [6 * delta3, 0, 0, 0],
            ]
        )

    def getGBSpline(self, p0: Point, p1: Point, p2: Point, p3: Point) -> BSplineGeoMatrix:
        gb_spline_x = [[p0.x], [p1.x], [p2.x], [p3.x]]
        gb_spline_y = [[p0.y], [p1.y], [p2.y], [p3.y]]

        return BSplineGeoMatrix(gb_spline_x, gb_spline_y)

    def getInitialCurve(self, delta_matrix: np.array, gb: BSplineGeoMatrix) -> tuple:
        cx = np.dot(self.BSPLINE_MATRIX, gb.x)
        cx = np.dot(delta_matrix, cx)

        cy = np.dot(self.BSPLINE_MATRIX, gb.y)
        cy = np.dot(delta_matrix, cy)

        return cx, cy

    def forward_difference(self, n: int, dx: np.array, dy: np.array, window, painter) -> None:
        x, dx, d2x, d3x = [x[0] for x in dx]
        y, dy, d2y, d3y = [y[0] for y in dy]

        #print("Inside Forwarad Differences dx", x,dx,d2x,d3x)
        #print("Inside Forwarad Differences dy", y,dy,d2y,d3y)

        i = 1

        x_old = x
        y_old = y

        while i < n:
            i += 1

            x += dx
            dx += d2x
            d2x += d3x

            y += dy
            dy += d2y
            d2y += d3y


            x1, y1 = self._normalize(x_old, y_old, window)
            x2, y2 = self._normalize(x, y, window)

            #print("NORMALIZED POINTS:", x1, y1, x2, y2)

            x1, y1, x2, y2 = curveClip(x1, y1, x2, y2, window)

            #print("POINTS AFTER CURVE CLIPE", x1, y1, x2, y2)

            #print("called _drawlines")
            self._drawLines(x1, y1, x2, y2, painter, window)

            x_old = x
            y_old = y


    def _normalize(self, x, y, window):
        yw_min, yw_max, xw_min, xw_max = window.getMinsAndMaxes()
        normal_x = (x - xw_min) / (xw_max - xw_min) * 2 - 1
        normal_y = (y - yw_min) / (yw_max - yw_min) * 2 - 1
        return (normal_x, normal_y)


    def _drawLines(self, x1, y1, x2, y2, painter, window):
        if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
            x1, y1 = viewportTransformation(x1, y1, window)
            x2, y2 = viewportTransformation(x2, y2, window)
            #print("called _drawlines")
            painter.drawLine(x1, y1, x2, y2)

    def transform(self, matrix: list) -> None:
        for point in self.__control_points:
            mult = np.matmul(np.array([point.x_normalized, point.y_normalized, 1]), matrix)
            point.x = mult.item(0)
            point.y = mult.item(1)

    def getCenter(self) -> list:
        sum_x = 0
        sum_y = 0
        for point in self.__control_points:
            sum_x += point.getX()
            sum_y += point.getY()

        return [sum_x / len(self.__control_points), sum_y / len(self.__control_points)]

    def transformToView(self):
        pass