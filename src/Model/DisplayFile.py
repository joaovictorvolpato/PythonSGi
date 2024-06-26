from src.Model.Window import Window
from src.Model.Point import Point
from src.Model.Point3D import Point3D
from src.Model.Line import Line, Line3D
from src.Model.Bezier import Bezier
from src.Model.Drawable import Drawable
from src.Model.WireFrame import Wireframe, WireFrame3D
from src.Model.BSpline import BSpline



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
        self.__curves = []
        self.__objects3D = []
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
    def curves(self) -> List[Bezier]:
        return self.__curves

    @property
    def objects3D(self) -> List[WireFrame3D]:
        return self.__objects3D

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

        if objectType == "BEZIER":
            if self.__buffer is not None:
                self.__buffer.append(buffer)
            else:
                self.__buffer = [buffer]

        if objectType == "BSPLINE":
            if self.__buffer is not None:
                self.__buffer.addControlPoint(buffer)
            else:
                self.__buffer = BSpline(first_control_point=buffer, window=windowP, color = object_color)

    def registerObject(self, currentType: str, objectName: str, object_color) -> None:
        if isinstance(self.__buffer, list):
            self.__curves.append(
                Bezier(
                    name=objectName,
                    coordinates=self.__buffer,
                    color=object_color,
                    window=Window(),
                )
            )
            self.__buffer = None

        elif isinstance(self.__buffer, BSpline):
            self.__curves.append(self.__buffer)
            self.__buffer = None

        elif isinstance(self.__buffer,Point):
            self.__points.append(self.__buffer)
            self.__buffer = None

        elif isinstance(self.__buffer,Line):
            print("Registering line: ", self.__buffer.start, self.__buffer.end)
            self.__lines.append(self.__buffer)
            self.__buffer = None
        elif isinstance(self.__buffer,Wireframe):
            self.__wireframes.append(self.__buffer)
            self.__buffer = None

    def create3DObject(self, points: List[tuple], edges: List[tuple], obj_name: str, objectsList):
        lines = []
        for point in points:
            #print(point[0], point[1], point[2])
            point3d = Point3D(point[0], point[1], point[2], window=self.__window)
            self.__points.append(point3d)
        for edge in edges:
            line = Line3D(self.__points[edge[0]], window=self.__window)
            line.start = self.__points[edge[0]]
            line.end = self.__points[edge[1]]
            lines.append(line)
            #print("line drawn between", self.__points[edge[0]], self.__points[edge[1]])
        wire3d = WireFrame3D(lines, name=obj_name)
        self.__objects3D.append(wire3d)

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

        for i, curve in enumerate(self.__curves):
            if curve.name == name:
                del self.__curves[i]
                return

    def getObjects(self) -> List[Drawable]:
        if self.__buffer is not None:
            return self.__points + self.__lines + self.__wireframes + [self.__buffer]
        return self.__points + self.__lines + self.__wireframes

    def get_buffer(self):
        return self.__buffer

    def confirmLastObject(self) -> None:
        self.__confirmed_last_one = True

    def setObjectName(self, objectName: str, object_color) -> None:
        if self.__buffer is None:
            return

        if not isinstance(self.__buffer, list):
            self.__buffer.name = objectName

        self.registerObject(self.__buffer, objectName, object_color)

    def tryRegistering(self, currentType: str, objectName: str, object_color) -> str:
        if self.__buffer is None:
            return {"status": False, "mensagem": "[ERROR] Draw an object first."}

        self.setObjectName(objectName, object_color)
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

        for curve in self.__curves:
            if curve.name == name:
                return curve

        for obj3d in self.__objects3D:
            if obj3d.name == name:
                return obj3d

    def addObjectFromFile(self, obj: Union[Point,Line,Wireframe,Point3D,Line3D]):
        print("OBJECT INSIDE ADD OBJECT FROM FILE", obj)
        if isinstance(obj, Point):
            self.__points.append(obj)
        elif isinstance(obj, Line):
            self.__lines.append(obj)
        elif isinstance(obj, WireFrame3D):
            print("Adding 3D object")
            self.__objects3D.append(obj)
        elif isinstance(obj, Wireframe):
            print("Adding object")
            self.__wireframes.append(obj)
        #elif isinstance(obj, Point3D):
        #    self.__objects3D.append(obj)
        #elif isinstance(obj, Line3D):
        #    self.__objects3D.append(obj)


    def normalizeObject(self, object):
        x = object.x
        y = object.y
        yw_min, yw_max, xw_min, xw_max = self.__window.getMinsAndMaxes()
        normal_x = (x - xw_min) / (xw_max - xw_min) * 2 - 1
        normal_y = (y - yw_min) / (yw_max - yw_min) * 2 - 1
        return (normal_x, normal_y)
