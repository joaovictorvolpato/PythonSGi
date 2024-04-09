from src.Model.Window import Window
import src.Model.Utils.consts as consts


# transforms the positions in the window to a Viewport usable
def viewportTransformation(x, y, window: Window):
    return _transformPoint(x, y, window)


def _transformPoint(x, y, window: Window) -> list:
    xw_min = -1
    yw_min = -1
    xw_max = 1
    yw_max = 1

    xv = (x - xw_min) / (xw_max - xw_min)
    xv *= consts.VIEWPORT_X_MAX- consts.VIEWPORT_X_MIN

    yv = 1 - (y - yw_min) / (yw_max - yw_min)
    yv *= consts.VIEWPORT_Y_MAX- consts.VIEWPORT_Y_MIN

    return round(xv), round(yv)

#For future use in case we want to transform from viewport to world coordinates
def transformToWorldCoordinates(x: float, y: float, window: Window):
    multx = consts.VIEWPORT_X_MAX - consts.VIEWPORT_X_MIN
    multy = consts.VIEWPORT_Y_MAX - consts.VIEWPORT_Y_MIN

    xw = window.xw_min + (x - consts.VIEWPORT_X_MIN) / multx * (
        window.xw_max - window.xw_min
    )
    yw = window.yw_min + (1 - (y - consts.VIEWPORT_Y_MIN) / multy) * (
        window.yw_max - window.yw_min
    )

    return round(xw), round(yw)