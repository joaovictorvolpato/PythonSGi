from Model.Patterns.singleton import SingletonMeta
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget


class View(QWidget):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Hello World!")
        self.show()

