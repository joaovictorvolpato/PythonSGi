from src.Model.Window import Window
from src.Model.Point import Point
from src.Model.Line import Line
from src.Model.Drawable import Drawable
from src.Model.WireFrame import Wireframe

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
        self.__confirmed_last_one = True

    @property
    def points(self):
        return self.__points

    @property
    def lines(self):
        return self.__lines

    @property
    def wireframes(self):
        return self.__wireframes

    def addToBuffer(self, objectType: str, buffer, windowP, objectName: str) -> None:
        print("Adding to buffer: ", objectType, buffer, windowP)
        if objectType == "POINT":
            self.__buffer = Point(buffer.x, buffer.y, window=windowP)
            print(self.__confirmed_last_one)
            if self.__confirmed_last_one:
                #self.registerObject("POINT", objectName, "black")
                self.__confirmed_last_one = False

        if objectType == "LINE":
            if self.__buffer is not None:
                print("!!!!!!!!!!!!!!!!!Adding end point to line!!!!!!!!!!!!!")
                self.__buffer.end  = buffer
                #self.registerObject("LINE", objectName, "black")
            else:
                print("Creating new line")
                self.__buffer = Line(buffer, window=windowP)

        if objectType == "WIREFRAME":
            if self.__buffer is not None:
                self.__buffer.points.append(buffer)
                self.__wireframes.append(self.__buffer)
            else:
                self.__buffer = Wireframe(buffer, window=windowP)

    def registerObject(self, currentType: str, objectName: str, color) -> None:

        if isinstance(self.__buffer,Point):
            self.__points.append(self.__buffer)
            self.__buffer = None
        elif isinstance(self.__buffer,Line):
            print("Registering line: ", self.__buffer.start, self.__buffer.end)
            self.__lines.append(self.__buffer)
            self.__buffer = None

        elif currentType == "WIREFRAME":
            self.__wireframes.append(self.__buffer)

    def deleteObject(self, name: str) -> None:
        for i, point in enumerate(self.__points):
            if point.name == name:
                print("Deleting point: ", point.name)
                del self.__points[i]
                return

        for i, line in enumerate(self.__lines):
            if line.name == name:
                del self.__lines[i]
                return

        for i, wireframe in enumerate(self.__wireframes):
            if wireframe.name == name:
                del self.__wireframes[i]
                return

    def getObjects(self) -> List[Drawable]:
        return self.__points + self.__lines + self.__wireframes

    def get_buffer(self):
        return self.__buffer
    
    def confirmLastObject(self) -> None:
        self.__confirmed_last_one = True

    def setObjectName(self, objectName: str, color) -> None:
        if self.__buffer is None:
            return

        self.__buffer.name = objectName
        self.registerObject(self.__buffer, objectName, color)

    def tryRegistering(self, currentType: str, objectName: str) -> str:
        if self.__buffer is None:
            return {"status": False, "mensagem": f"[ERROR] Draw an object first."}

        self.setObjectName(objectName, "black")
        return {"status": True, "mensagem": f"{objectName} ({currentType}) registered."}
