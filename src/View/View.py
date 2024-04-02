
from PyQt5.QtWidgets import (
     QMainWindow
)

from PyQt5 import QtCore, QtGui, QtWidgets


from src.View.main_ui import Ui_Dialog
from src.Controllers.Controller import Controller
from src.View.transformations import Transformations

class View(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__controller = Controller()
        self.setupUi(self)
        self.__controller.attach_viewport(self.ViewPort)
        self.attach_controllerUI(self.__controller)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.pushButton_3.clicked.connect(lambda: self.navigate('UP'))
        self.pushButton_4.clicked.connect(lambda: self.navigate('RIGHT'))
        self.pushButton_5.clicked.connect(lambda: self.navigate('DOWN'))
        self.pushButton_6.clicked.connect(lambda: self.navigate('LEFT'))
        self.comboBox.currentIndexChanged.connect(self.changeObjectType)
        self.pushButton.clicked.connect(lambda: self.zoom('IN'))
        self.pushButton_2.clicked.connect(lambda: self.zoom('OUT'))
        self.deleteButton.clicked.connect(self.deleteObject)
        self.confirmButton.clicked.connect(lambda: self.confirmObject(self.lineEdit.text()))
        self.lineEdit.textChanged.connect(lambda: self.setObjectName(self.lineEdit.text()))
        self.listWidget.doubleClicked.connect(lambda: self.openTransformationModal(self.listWidget.currentItem().text()))

    def navigate(self, direction: str):
        self.__controller.navigate(direction)

    def changeObjectType(self, index):
        # Implemente a lógica para mudar o tipo de objeto
        switcher = {
            0: "Point",
            1: "Line",
            2: "Wireframe"
        }

        self.__controller.selected_object = switcher[index]
        print('changeObjectType')
        print(index)

    def zoom(self, direction):
        self.__controller.zoom(direction)

    def deleteObject(self) -> None:
        list_item = self.listWidget.currentRow()
        if list_item is not None:
            object_name = self.listWidget.item(list_item).text()
            self.__controller.deleteObject(object_name)
            self.listWidget.takeItem(list_item)

    def confirmObject(self, name: str):
        dict = self.__controller.createObject()
        if dict["status"] == True:
            self.listWidget.addItem(name)
            self.lineEdit.clear()

    def setObjectName(self, name: str):
        print(name)
        self.__controller.object_name = name

    def openTransformationModal(self, objectName: str):
        self.window = QtWidgets.QMainWindow()
        self.ui = Transformations()
        self.ui.setupUi(
            self.window,
            currentObject=self.__controller.display_file.getObjectByName(objectName),
            updateObject=self.__controller.update(),
            closeModal=self.window.close,
        )
        self.window.show()