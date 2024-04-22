import numpy as np

from src.Model.Point import Point
from typing import List

BEZIER_MATRIX = [[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 3, 0, 0], [1, 0, 0, 0]]


class BezierGeoMatrix:
    def __init__(self, x: List[List[float]], y: [List[List[float]]]):
        self.x = x
        self.y = y


def getGBBezier(p0: Point, p1: Point, p2: Point, p3: Point) -> BezierGeoMatrix:
    gb_x = [[p0.x], [p1.x], [p2.x], [p3.x]]

    gb_y = [[p0.y], [p1.y], [p2.y], [p3.y]]

    return BezierGeoMatrix(gb_x, gb_y)


def blendingFunction(t: float, gb: List[List[float]]) -> float:
    m_t = [[t**3, t**2, t, 1]]
    blending = np.dot(m_t, BEZIER_MATRIX)

    return np.dot(blending, gb)[0][0]
