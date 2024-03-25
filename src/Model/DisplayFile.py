from src.Model.Window import Window
from src.Model.Point import Point
from src.Model.Line import Line
from src.Model.Drawable import Drawable

from src.Model.Patterns.singleton import SingletonMeta

from typing import List



class SingletonClass(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance


class DisplayFile(SingletonClass):
    def __init__(self):
        print("DisplayFile created")
        print(self)
        self.__points = []
        self.__lines = []
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
    
    def addToBuffer(self, objectType: str, buffer, windowP) -> None:
        print("Adding to buffer: ", objectType, buffer, windowP)
        if objectType == "POINT":
            self.__buffer = Point(buffer, window=windowP)
            self.registerObject("POINT", "Point", "black")

        if objectType == "LINE":
            if self.__buffer is not None:
                print("!!!!!!!!!!!!!!!!!Adding end point to line!!!!!!!!!!!!!")
                self.__buffer.end  = buffer
                self.registerObject("LINE", "Line", "black")
            else:
                print("Creating new line")
                self.__buffer = Line(buffer, window=windowP)
                

    
    def registerObject(self, currentType: str, objectName: str, color) -> None:
        if currentType == "POINT":
            self.__points.append(self.__buffer)
        elif currentType == "LINE":
            print("Registering line: ", self.__buffer.start, self.__buffer.end)
            self.__lines.append(self.__buffer)
            print(self)
        elif currentType == "WIREFRAME":
            self.__wireframes.append(self.__buffer)

        self.__buffer = None

    def getObjects(self) -> List[Drawable]:
        return self.__points + self.__lines + self.__wireframes
    
    def get_buffer(self):
        return self.__buffer
