from src.Model.Utils import consts

from src.Model.Patterns.singleton import Singleton


class Window(Singleton):
    def __init__(self):
        if not super().created:
            self.xw_min = consts.VIEWPORT_X_MIN
            self.yw_min = consts.VIEWPORT_Y_MIN
            self.xw_max = consts.VIEWPORT_X_MAX
            self.yw_max = consts.VIEWPORT_Y_MAX

            self.step = 10  # amount of pixels
            self.rotation_zoom_percentage = 10
            self.rotation_amount = 10
            self.windowInstance = self


    @property
    def xw_min(self):
        return self.__xw_min

    @xw_min.setter
    def xw_min(self, xw_min):
        self.__xw_min = xw_min

    @property
    def yw_min(self):
        return self.__yw_min

    @yw_min.setter
    def yw_min(self, yw_min):
        self.__yw_min = yw_min

    @property
    def xw_max(self):
        return self.__xw_max

    @xw_max.setter
    def xw_max(self, xw_max):
        self.__xw_max = xw_max

    @property
    def yw_max(self):
        return self.__yw_max

    @yw_max.setter
    def yw_max(self, yw_max):
        self.__yw_max = yw_max

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

    def getCenter(self):
        return ((self.xw_max + self.xw_min)/2, (self.yw_max + self.yw_min)/2)

    def getMinsAndMaxes(self):
        return [self.yw_min, self.yw_max, self.xw_min, self.xw_max]
