from src.Model.DisplayFile import DisplayFile
from src.Model.Window import Window
from src.Model.Viewport import Viewport
from src.Model.Patterns.observer import Observer
from src.Model.Utils.ViewPortTransform import transformToWorldCoordinates
from src.Model.Point import Point

class Controller(Observer):
    def __init__(self):
        self.__display_file = DisplayFile()
        self.__window = Window()
        self.__view_port = None
        self.__selected_object = "Point"

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

    def update(self):
        print("Controller updated, draw {} at {} {}".format(self.__selected_object, self.__view_port.clicked_x, self.__view_port.clicked_y))
        x, y = transformToWorldCoordinates(
            self.__view_port.clicked_x, self.__view_port.clicked_y, self.__window
        )

        point = Point(x, y, self.window)

        print("Point: ", point.x, point.y)

        print("Selected object: ", self.selected_object)

        print("called getObjects in controller  ", self.display_file.getObjects())

        if self.selected_object == "Point":
            self.display_file.addToBuffer(
                "POINT",
                point,
                self.window
            )

        elif self.selected_object == "Line":
            print("Adding line to buffer")
            self.display_file.addToBuffer(
                "LINE",
                point,
                self.window
            )
        elif self.selected_object == "Wireframe":
            self.display_file.addToBuffer(
                "WIREFRAME",
                point,
                self.window
            )
        self.__view_port.update()

    def navigate(self, direction: str):
        self.__window.navigate(direction)
        self.__view_port.update()

    def zoom(self, direction: str):
        self.__window.zoom(direction)
        self.__view_port.update()

    def confirmObject(self, name: str):
        dict = self.__display_file.tryRegistering(
            self.selected_object, name
        )

        return dict

    def deleteObject(self, name: str):
        self.__display_file.deleteObject(name)
        self.__view_port.update()


