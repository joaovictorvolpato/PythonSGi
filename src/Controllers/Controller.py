from PyQt5 import QtCore

from src.Model.DisplayFile import DisplayFile
from src.Model.MatrixOperations import MatrixOperations
from src.Model.Window import Window
from src.Model.Viewport import Viewport
from src.Model.Patterns.observer import Observer
from src.Model.Utils.ViewPortTransform import transformToWorldCoordinates
from src.Model.Point import Point

class Controller(Observer):
    def __init__(self):
        self.__display_file = DisplayFile()
        self.__window = Window()
        self.__matrix_operations = MatrixOperations()
        self.__view_port = None
        self.__selected_object = "Point"
        self.__object_name = ""
        self.__object_color = None

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
