from src.Model.Utils import consts


class Window:
    def __init__(self):
        self.xw_min = consts.VIEWPORT_X_MIN
        self.yw_min = consts.VIEWPORT_Y_MIN
        self.xw_max = consts.VIEWPORT_X_MAX
        self.yw_max = consts.VIEWPORT_Y_MAX

        self.step = 10  # amount of pixels
        self.rotation_zoom_percentage = 10

    def getOrigin(self):
        return self.xw_min, self.yw_min

    def zoom(self, direction: str):
        if direction == "OUT":
            zoomAmount = 1 + self.rotation_zoom_percentage / 100
        else:
            zoomAmount = 1 - self.rotation_zoom_percentage / 100

        self.xw_min *= zoomAmount
        self.yw_min *= zoomAmount
        self.xw_max *= zoomAmount
        self.yw_max *= zoomAmount

    def navigate(self, direction):
        if direction == "UP":
            self.yw_min += self.step
            self.yw_max += self.step
        elif direction == "DOWN":
            self.yw_min -= self.step
            self.yw_max -= self.step
        elif direction == "RIGHT":
            self.xw_min += self.step
            self.xw_max += self.step
        elif direction == "LEFT":
            self.xw_min -= self.step
            self.xw_max -= self.step
