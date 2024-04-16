
from src.Model.DisplayFile import DisplayFile
from src.Model.Drawable import Drawable
from src.Model.Point import Point
from src.Model.Patterns.strategy import Strategy
from typing import List
from src.Model.Line import Line
from src.Model.Window import Window


from enum import Enum

class Position(Enum):
    INSIDE = 0  # 0000
    LEFT = 1  # 0001
    RIGHT = 2  # 0010
    BOTTOM = 4  # 0100
    TOP = 8  # 1000

class CohenSutherland(Strategy):
    def __init__(self) -> None:
        super().__init__()

    def clipping_algorithm(self, line: Line, windowobj: Window, boarder = 20) -> Line:
        window_max = Point(windowobj.xw_max, windowobj.yw_max, window=Window())
        window_min = Point(windowobj.xw_min, windowobj.yw_min, window=Window())

        window_min.x = window_min.x + boarder
        window_min.y = window_min.y + boarder

        window_min.normalizePoint()
        window_max.x = window_max.x - boarder
        window_max.y = window_max.y - boarder
        window_max.normalizePoint()
        window = {"xw_min": window_min.x_normalized, "yw_min": window_min.y_normalized, "xw_max": window_max.x_normalized, "yw_max": window_max.y_normalized}

        point1, point2 = line.points[0], line.points[1]
        point1.normalizePoint()
        point2.normalizePoint()
        rc_point1 = self._getRegionCode(point1, window)
        rc_point2 = self._getRegionCode(point2, window)

        while True:
            if rc_point1 == 0 and rc_point2 == 0:
                line.setNormalCoordinates(point1, point2)
                return line
            elif (rc_point1 & rc_point2) != 0:
                return None

            else:
                newX, newY = 0, 0

                if rc_point1 != 0:
                    rc_out = rc_point1
                else:
                    rc_out = rc_point2

                if rc_out & Position.TOP.value:
                    newX = point1.x_normalized + (
                        point2.x_normalized - point1.x_normalized
                    ) * (window["yw_max"] - point1.y_normalized) / (
                        point2.y_normalized - point1.y_normalized
                    )
                    newY = window["yw_max"]

                elif rc_out & Position.BOTTOM.value:
                    newX = point1.x_normalized + (
                        point2.x_normalized - point1.x_normalized
                    ) * (window["yw_min"] - point1.y_normalized) / (
                        point2.y_normalized - point1.y_normalized
                    )
                    newY = window["yw_min"]

                elif rc_out & Position.RIGHT.value:
                    newY = point1.y_normalized + (
                        point2.y_normalized - point1.y_normalized
                    ) * (window["xw_max"] - point1.x_normalized) / (
                        point2.x_normalized - point1.x_normalized
                    )
                    newX = window["xw_max"]

                elif rc_out & Position.LEFT.value:
                    newY = point1.y_normalized + (
                        point2.y_normalized - point1.y_normalized
                    ) * (window["xw_min"] - point1.x_normalized) / (
                        point2.x_normalized - point1.x_normalized
                    )
                    newX = window["xw_min"]

                if rc_out == rc_point1:
                    point1 = Point(point1.x, point1.y, Window())
                    point1.setNormalCoordinates(newX, newY)
                    rc_point1 = self._getRegionCode(point1, window)
                else:
                    point2 = Point(point2.x, point2.y, Window())
                    point2.setNormalCoordinates(newX, newY)
                    rc_point2 = self._getRegionCode(point2, window)


    def _getRegionCode(self, point1: Point, window: dict) -> int:
        x, y = point1.x_normalized, point1.y_normalized
        rc = Position.INSIDE.value

        if x > window["xw_max"]:
            rc |= Position.RIGHT.value
        elif x < window["xw_min"]:
            rc |= Position.LEFT.value

        if y > window["yw_max"]:
            rc |= Position.TOP.value
        elif y < window["yw_min"]:
            rc |= Position.BOTTOM.value

        return rc


class LiangBarsky(Strategy):
    def __init__(self) -> None:
        super().__init__()

    def clipping_algorithm(self, line: Line, windowobj: Window, boarder = 20) -> Line:
        window_max = Point(windowobj.xw_max, windowobj.yw_max, window=Window())
        window_min = Point(windowobj.xw_min, windowobj.yw_min, window=Window())

        window_min.x = window_min.x + boarder
        window_min.y = window_min.y + boarder

        window_min.normalizePoint()
        window_max.x = window_max.x - boarder
        window_max.y = window_max.y - boarder
        window_max.normalizePoint()

        p1, p2 = line.points
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        p = [-dx, dx, -dy, dy]
        q = [p1.x - window_min.x, window_max.x - p1.x, p1.y - window_min.y, window_max.y - p1.y]

        u1 = 0
        u2 = 1

        for i in range(4):
            if p[i] == 0:
                if q[i] < 0:
                    return None
            else:
                u = q[i] / p[i]
                if p[i] < 0:
                    u1 = max(u1, u)
                else:
                    u2 = min(u2, u)

        if u1 > u2:
            return None

        x1 = p1.x + u1 * dx
        y1 = p1.y + u1 * dy
        x2 = p1.x + u2 * dx
        y2 = p1.y + u2 * dy

        line.setNormalCoordinates(Point(x1, y1,window=Window()), Point(x2, y2,window=Window()))
        return line


liangBarsky = LiangBarsky()
cohenSutherland = CohenSutherland()
