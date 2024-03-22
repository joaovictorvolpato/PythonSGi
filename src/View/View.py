from src.Controllers.Controller import Controller
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget

class View(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__controller = Controller()
        self.setWindowTitle("Hello World!")
        self.show()

