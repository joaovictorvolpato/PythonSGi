from Drawable import Drawable
from Point import Point

from Patterns.observer import Observed

class Line(Drawable, Observed):
    def __init__(self, start:Point, end:Point, name:str = None, controller:str = None) -> None:
        super().__init__(name)
        self.__start = start
        self.__end = end
        self.attach(controller)

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

    def draw(self):
        pass

    def transformToView(self):
        pass    