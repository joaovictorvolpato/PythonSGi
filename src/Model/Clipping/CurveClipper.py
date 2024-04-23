from src.Model.Window import Window
from src.Model.Point import Point

INSIDE = 0  # 0000
LEFT = 1  # 0001
RIGHT = 2  # 0010
BOTTOM = 4  # 0100
TOP = 8  # 1000


def curveClip(x1, y1, x2, y2, windowobj: Window):

    boarder = 20

    window_max = Point(windowobj.xw_max, windowobj.yw_max, window=Window())
    window_min = Point(windowobj.xw_min, windowobj.yw_min, window=Window())

    window_min.x = window_min.x + boarder
    window_min.y = window_min.y + boarder

    window_min.normalizePoint()
    window_max.x = window_max.x - boarder
    window_max.y = window_max.y - boarder
    window_max.normalizePoint()

    x_min = window_min.x_normalized
    y_min = window_min.y_normalized
    x_max = window_max.x_normalized
    y_max = window_max.y_normalized

    rc1 = _getRegionCode(x1, y1, x_max, x_min, y_max, y_min)
    rc2 = _getRegionCode(x2, y2, x_max, x_min, y_max, y_min)

    while True:
        if rc1 == 0 and rc2 == 0:
            return x1, y1, x2, y2

        elif (rc1 & rc2) != 0:
            return None, None, None, None

        else:
            new_x = 1
            new_y = 1

            if rc1 != 0:
                rc_out = rc1
            else:
                rc_out = rc2

            if rc_out & TOP:
                new_x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                new_y = y_max

            elif rc_out & BOTTOM:
                new_x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                new_y = y_min

            elif rc_out & RIGHT:
                new_y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                new_x = x_max

            elif rc_out & LEFT:
                new_y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                new_x = x_min

            if rc_out == rc1:
                x1 = new_x
                y1 = new_y
                rc1 = _getRegionCode(new_x, new_y, x_max, x_min, y_max, y_min)
            else:
                x2 = new_x
                y2 = new_y
                rc2 = _getRegionCode(new_x, new_y, x_max, x_min, y_max, y_min)


def _getRegionCode(x, y, x_max, x_min, y_max, y_min):
    region_code = INSIDE

    if x > x_max:
        region_code |= RIGHT
    elif x < x_min:
        region_code |= LEFT

    if y > y_max:
        region_code |= TOP
    elif y < y_min:
        region_code |= BOTTOM

    return region_code
