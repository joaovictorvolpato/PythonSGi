from src.Model.DisplayFile import DisplayFile
from src.Model.Window import Window
from src.Model.Viewport import Viewport
from src.Model.Patterns.observer import Observer

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
        self.__view_port.update()
    
    def navigate(self, direction: str):
        self.__window.navigate(direction)
        self.__view_port.update()

    def handleConfirmClick(self, name: str) -> None:
        if name == "":
            self.openFileModal()
            return

        dict = self.__display_file.tryRegistering(
            self.viewport.currentSelectedType, name, self.__currentColor
        )
        self.logField.addItem(dict["mensagem"])
        if dict["status"] == True:
            self.objectsList.addItem(name)
            self.objectNameInput.clear()
        self.viewport.update()
