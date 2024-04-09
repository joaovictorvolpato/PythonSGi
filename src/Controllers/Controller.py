from PyQt5 import QtCore

from src.Model.DisplayFile import DisplayFile
from src.Model.MatrixOperations import MatrixOperations
from src.Model.Window import Window
from src.Model.Viewport import Viewport
from src.Model.Patterns.observer import Observer
from src.Model.Utils.ViewPortTransform import transformToWorldCoordinates
from src.Model.Point import Point
from src.Model.Utils.saveFile import saveFile
from src.Model.Drawable import Drawable

class Controller(Observer):
    def __init__(self):
        self.__display_file = DisplayFile()
        self.__window = Window()
        self.__matrix_operations = MatrixOperations()
        self.__view_port = None
        self.__selected_object = "Point"
        self.__object_name = ""
        self.__object_color = None
        self.__objectsList = []
        self.__file_modal = None

    def attach_viewport(self, view_port: Viewport):
        print("Controller viewport attached to controller")
        self.__view_port = view_port

    @property
    def display_file(self):
        return self.__display_file

    @property
    def window(self):
        return self.__window

    @property
    def view_port(self):
        return self.__view_port

    @property
    def selected_object(self):
        return self.__selected_object

    @selected_object.setter
    def selected_object(self, selected_object: str):
        self.__selected_object = selected_object

    @property
    def object_name(self):
        return self.__object_name

    @object_name.setter
    def object_name(self, object_name: str):
        self.__object_name = object_name

    @property
    def object_color(self):
        return self.__object_color

    @object_color.setter
    def object_color(self, object_color: str):
        print("Setting object color to ", object_color)
        self.__object_color = object_color

    @property
    def objectsList(self):
        return self.__objectsList

    @objectsList.setter
    def objectsList(self, objectsList: list):
        self.__objectsList = objectsList

    @property
    def file_modal(self):
        return self.__file_modal

    @file_modal.setter
    def file_modal(self, file_modal):
        self.__file_modal = file_modal

    def update(self):
        print("Controller updated, draw {} at {} {}".format(self.__selected_object, self.__view_port.clicked_x, self.__view_port.clicked_y))
        x, y = transformToWorldCoordinates(
            self.__view_port.clicked_x, self.__view_port.clicked_y, self.__window
        )

        point = Point(x, y, self.window, self.object_color)

        print("Point: ", point.x, point.y)

        print("Selected object: ", self.selected_object)

        print("called getObjects in controller  ", self.display_file.getObjects())

        if self.selected_object == "Point":
            self.display_file.addToBuffer(
                "POINT",
                point,
                self.window,
                self.object_color
            )

        elif self.selected_object == "Line":
            print("Adding line to buffer")
            self.display_file.addToBuffer(
                "LINE",
                point,
                self.window,
                self.object_color
            )
        elif self.selected_object == "Wireframe":
            self.display_file.addToBuffer(
                "WIREFRAME",
                point,
                self.window,
                self.object_color
            )
        self.__view_port.update()

    def navigate(self, direction: str):
        self.__window.navigate(direction)
        self.__view_port.update()

    def zoom(self, direction: str):
        self.__window.zoom(direction)
        self.__view_port.update()

    def createObject(self):
        if self.selected_object == "Point":
            self.__display_file.confirmLastObject()

        dict = self.__display_file.tryRegistering(
            self.selected_object, self.object_name
        )

        self.view_port.update()

        return dict

    def deleteObject(self, name: str):
        self.__display_file.deleteObject(name)
        self.__view_port.update()

    def transformObject(self, name: str, transformation: dict):
        print("Transforming object: ", name, transformation)
        if transformation["type"] == "scaling":
            object_to_transform = self.__display_file.getObjectByName(name)
            center = object_to_transform.getCenter()
            matrix1 = self.__matrix_operations.build_translation_matrix(
                -center[0], -center[1]
            )
            matrix2 = self.__matrix_operations.build_scaling_matrix(
                float(transformation["sx"]), float(transformation["sy"])
            )
            matrix3 = self.__matrix_operations.build_translation_matrix(
                center[0], center[1]
            )
            matrix = self.__matrix_operations.matrix_composition(
                [matrix1, matrix2, matrix3]
            )
        if transformation["type"] == "rotation":
            if transformation["center"] == "object":
                object_to_transform = self.__display_file.getObjectByName(name)
                center = object_to_transform.getCenter()
                matrix1 = self.__matrix_operations.build_translation_matrix(
                    -center[0], -center[1]
                )
                matrix2 = self.__matrix_operations.build_rotation_matrix(
                    float(transformation["angle"])
                )
                matrix3 = self.__matrix_operations.build_translation_matrix(
                    center[0], center[1]
                )
                matrix = self.__matrix_operations.matrix_composition(
                    [matrix1, matrix2, matrix3]
                )
            elif transformation["center"] == "origin":
                center = self.__window.getOrigin()
                matrix1 = self.__matrix_operations.build_translation_matrix(
                    -center[0], -center[1]
                )
                matrix2 = self.__matrix_operations.build_rotation_matrix(
                    float(transformation["angle"])
                )
                matrix3 = self.__matrix_operations.build_translation_matrix(
                    center[0], center[1]
                )
                matrix = self.__matrix_operations.matrix_composition(
                    [matrix1, matrix2, matrix3]
                )
            elif transformation["center"] == "point":
                x = transformation["pointx"]
                y = transformation["pointy"]
                matrix1 = self.__matrix_operations.build_translation_matrix(
                    -int(x), -int(y)
                )
                matrix2 = self.__matrix_operations.build_rotation_matrix(
                    float(transformation["angle"])
                )
                matrix3 = self.__matrix_operations.build_translation_matrix(
                    int(x), int(y)
                )
                matrix = self.__matrix_operations.matrix_composition(
                    [matrix1, matrix2, matrix3]
                )
        if transformation["type"] == "translation":
            matrix = self.__matrix_operations.build_translation_matrix(
                transformation["tx"], transformation["ty"]
            )
        object_to_transform = self.__display_file.getObjectByName(name)
        object_to_transform.transform(matrix)
        self.__view_port.update()

    def rotate(self, direction: str):
        if direction == "LEFT":
            self.__window.rotate("LEFT")
        elif direction == "RIGHT":
            self.__window.rotate("RIGHT")
        self.__view_port.update()

    def setWindowDimensions(self, min, max):
        self.__window.xw_min = min[0]
        self.__window.yw_min = min[1]
        self.__window.xw_max = max[0]
        self.__window.yw_max = max[1]

    def saveObjectsToFile(self, filename: str) -> None:
        objects = []

        for point in self.__display_file.points:
            objects.append(point)
        for line in self.__display_file.lines:
            objects.append(line)
        for wireframe in self.__display_file.wireframes:
            objects.append(wireframe)

        window = self.__window
        w_min = Point(window.xw_min, window.yw_min)
        w_max = Point(window.xw_max, window.yw_max)

        saveFile(filename=filename, objects=objects, window=[w_min, w_max])
        self.file_modal.close()
    def _rotateObject(self, obj: Drawable, x, y, amount):
        translation = self.__matrix_operations.build_translation_matrix(
            -float(x),
            -float(y),
        )
        rotation_matrix = self.__matrix_operations.build_rotation_matrix(
            float(amount)
        )
        translate_back = self.__matrix_operations.build_translation_matrix(
            float(x),
            float(y),
        )
        matrix = self.__matrix_operations.matrix_composition(
                    [translation, rotation_matrix, translate_back]
                )
        obj.transform(matrix)

    def rotateWindow(self, direction: str, amount: str):
        x, y = self.__window.getCenter()

        if direction == "RIGHT":
            amount = -float(amount)

        points = self.__display_file.points

        for point in points:
            self._rotateObject(point.name, x, y, amount)

        for line in self.__display_file.lines:
            if (line.name != None):
                self._rotateObject(line, x, y, amount)

        for wireframe in self.__display_file.wireframes:
            self._rotateObject(wireframe, x, y, amount)

        self.__view_port.update()
