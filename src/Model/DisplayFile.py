from src.Model.Window import Window
from src.Model.Point import Point
from src.Model.Line import Line
from src.Model.Drawable import Drawable
from src.Model.WireFrame import Wireframe

from src.Model.Patterns.singleton import SingletonClass      


from typing import List
from typing import Union


class DisplayFile(SingletonClass):
    def __init__(self):
        print("DisplayFile created")
        #print(self)
        self.__points = []
        self.__lines = []
        self.__wireframes = []
        self.__buffer = None
        self.__confirmed_last_one = True
        self.__selected_clipping_algorithm = None

    @property
    def points(self) -> List[Point]:
        return self.__points

    @property
    def lines(self) -> List[Line]:
        return self.__lines

    @property
    def wireframes(self) -> List[Wireframe]:
        return self.__wireframes
    
    @property
    def selected_clipping_algorithm(self):
        return self.__selected_clipping_algorithm
    
    @selected_clipping_algorithm.setter
    def selected_clipping_algorithm(self, clipping_algorithm):
        self.__selected_clipping_algorithm = clipping_algorithm

    def addToBuffer(self, objectType: str, buffer, windowP, object_color: str, is_filled = False) -> None:
        if objectType == "POINT":
            self.__buffer = Point(buffer.x, buffer.y, window=windowP, color = object_color)
            print(self.__confirmed_last_one)
            if self.__confirmed_last_one:
                self.__confirmed_last_one = False

        if objectType == "LINE":
            if self.__buffer is not None:
                self.__buffer.end  = buffer
            else:
                self.__buffer = Line(buffer, window=windowP, color = object_color)

        if objectType == "WIREFRAME":
            if self.__buffer is not None:
                self.__buffer.addPoint(buffer)
            else:
                print(object_color)
                self.__buffer = Wireframe(buffer, window=windowP,color = object_color, is_filled=is_filled)

    def registerObject(self, currentType: str, objectName: str) -> None:

        if isinstance(self.__buffer,Point):
            self.__points.append(self.__buffer)
            self.__buffer = None
        elif isinstance(self.__buffer,Line):
            print("Registering line: ", self.__buffer.start, self.__buffer.end)
            self.__lines.append(self.__buffer)
            self.__buffer = None
        elif isinstance(self.__buffer,Wireframe):
            self.__wireframes.append(self.__buffer)
            self.__buffer = None

    def registerBoarder(self, line1, line2, line3, line4) -> None:
        self.__lines.append(line1)
        self.__lines.append(line2)
        self.__lines.append(line3)
        self.__lines.append(line4)

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
        if self.__buffer is not None:
            return self.__points + self.__lines + self.__wireframes + [self.__buffer]
        return self.__points + self.__lines + self.__wireframes

    def get_buffer(self):
        return self.__buffer

    def confirmLastObject(self) -> None:
        self.__confirmed_last_one = True

    def setObjectName(self, objectName: str) -> None:
        if self.__buffer is None:
            return

        self.__buffer.name = objectName
        self.registerObject(self.__buffer, objectName)

    def tryRegistering(self, currentType: str, objectName: str) -> str:
        if self.__buffer is None:
            return {"status": False, "mensagem": f"[ERROR] Draw an object first."}

        self.setObjectName(objectName)
        return {"status": True, "mensagem": f"{objectName} ({currentType}) registered."}

    def getObjectByName(self, name: str):
        for point in self.__points:
            if point.name == name:
                return point

        for line in self.__lines:
            if line.name == name:
                return line

        for wireframe in self.__wireframes:
            if wireframe.name == name:
                return wireframe

    def addObjectFromFile(self, obj: Union[Point,Line,Wireframe]):
        if isinstance(obj, Point):
            self.__points.append(obj)
        elif isinstance(obj, Line):
            self.__lines.append(obj)
        elif isinstance(obj, Wireframe):
            self.__wireframes.append(obj)

    def normalizeObject(self, object):
        x = object.x
        y = object.y
        yw_min, yw_max, xw_min, xw_max = self.__window.getMinsAndMaxes()
        normal_x = (x - xw_min) / (xw_max - xw_min) * 2 - 1
        normal_y = (y - yw_min) / (yw_max - yw_min) * 2 - 1
        return (normal_x, normal_y)
