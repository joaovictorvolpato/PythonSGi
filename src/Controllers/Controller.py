from src.Model.DisplayFile import DisplayFile
from src.Model.Window import Window
from src.Model.ViewPort import ViewPort

class Controller:
    def __init__(self):
        self.__display_file = DisplayFile()
        self.__window = Window()
        self.__view_port = ViewPort()
