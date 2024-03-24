from src.Model.Window import Window
from src.Model.Point import Point
from src.Model.Line import Line

from src.Model.Patterns.singleton import SingletonMeta

from typing import List


class DisplayFile(object):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

    def __init__(self):
        self.__points = List[Point]
        self.__lines = List[Line]
        self.__wireframes = []
        self.__buffer = None

    @property
    def points(self):
        return self.__points
    
    @property
    def lines(self):
        return self.__lines
    
    @property
    def wireframes(self):
        return self.__wireframes
    
    def addToBuffer(self, objectType: str, buffer) -> None:
        if objectType == "LINE":
            if self.__buffer is not None:
                self.__buffer.addPoint(buffer)
            else:
                self.__buffer = Line(buffer, window=self.__window)
