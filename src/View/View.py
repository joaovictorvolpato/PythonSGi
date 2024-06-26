
from PyQt5.QtWidgets import (
    QMainWindow
)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QColorDialog



from src.View.main_ui import Ui_Dialog
from src.Controllers.Controller import Controller
from src.View.transformations import Transformations
from src.View.fileModal import FileModal

class View(QMainWindow, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__controller = Controller()
        self.setupUi(self)
        self.__controller.attach_viewport(self.ViewPort)
        self.attach_controllerUI(self.__controller)
        self.connectSignalsSlots()
        self.__controller.draw_borders()

    def connectSignalsSlots(self):
        self.pushButton_3.clicked.connect(lambda: self.navigate('UP'))
        self.pushButton_4.clicked.connect(lambda: self.navigate('RIGHT'))
        self.pushButton_5.clicked.connect(lambda: self.navigate('DOWN'))
        self.pushButton_6.clicked.connect(lambda: self.navigate('LEFT'))
        self.pushButton_7.clicked.connect(lambda: self.navigate('Z-UP'))
        self.pushButton_8.clicked.connect(lambda: self.navigate('Z-DOWN'))
        self.comboBox.currentIndexChanged.connect(self.changeObjectType)
        self.pushButton.clicked.connect(lambda: self.zoom('IN'))
        self.pushButton_2.clicked.connect(lambda: self.zoom('OUT'))
        self.deleteButton.clicked.connect(self.deleteObject)
        self.confirmButton.clicked.connect(lambda: self.confirmObject(self.lineEdit.text()))
        self.lineEdit.textChanged.connect(lambda: self.setObjectName(self.lineEdit.text()))
        self.listWidget.doubleClicked.connect(lambda: self.openTransformationModal(self.listWidget.currentItem().text()))
        self.pushButton_color.clicked.connect(lambda: self.setColorObject())
        self.rotateLeftButton.clicked.connect(lambda: self.rotate('LEFT'))
        self.rotateRightButton.clicked.connect(lambda: self.rotate('RIGHT'))
        self.addFileButton.clicked.connect(self.openFile)
        self.fillObjectCheckbox.stateChanged.connect(self.fillObject)
        self.selectClipping.currentIndexChanged.connect(self.changeClipper)

    def navigate(self, direction: str):
        self.__controller.navigate(direction)

    def changeObjectType(self, index):
        switcher = {
            0: "Point",
            1: "Line",
            2: "Wireframe",
            3: "Bezier",
            4: "BSpline",
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
        if dict["status"] is True:
            self.listWidget.addItem(name)
            self.lineEdit.clear()

    def setObjectName(self, name: str):
        self.__controller.object_name = name

    def openTransformationModal(self, objectName: str):
        self.window = QtWidgets.QMainWindow()
        self.ui = Transformations()
        self.ui.setupUi(
            self.window,
            currentObject=self.__controller.display_file.getObjectByName(objectName),
            updateObject=self.__controller.update(),
            controller = self.__controller,
            closeModal=self.window.close
        )
        self.window.show()

    def setColorObject(self) -> None:
        self.__controller.object_color = QColorDialog.getColor()

    def rotate(self, direction: str):
        self.__controller.rotate(direction)

    def openFile(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = FileModal()
        self.ui.setupUi(
            self.window,
            closeModal=self.window.close,
            setWindowDimensions=self.__controller.setWindowDimensions,
            getObjectsFromFile=self.getObjectsFromFile,
            saveObjectsToFile=self.__controller.saveObjectsToFile,
            window = self.__controller.window
        )
        self.__controller.file_modal = self.window
        self.window.show()

    def getObjectsFromFile(self, objectsList: list):
        print("OBJECT LIST INSIDE GETOBJFROMFILE", objectsList)
        for obj in objectsList:
            print("OBJECT BEFORE SETTING WINDOW", obj)
            obj.window = self.__controller.window
            print("OBJECT AFTER SETTING WINDOW", obj)
            self.listWidget.addItem(obj.name)
            print("OBJECTNAME", obj)
            self.__controller.display_file.addObjectFromFile(obj)
            self.update()

    def fillObject(self):
        is_filled =  self.fillObjectCheckbox.isChecked()
        self.__controller.is_filled = is_filled

    def changeClipper(self, index):
        print(index)
        switcher = {
            0: "CohenSutherland",
            1: "LiangBarsky"
        }

        self.__controller.selected_clipping_algorithm = switcher[index]