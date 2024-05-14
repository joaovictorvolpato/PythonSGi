from os import listdir

from PyQt5 import QtCore, QtGui, QtWidgets

from src.Model.Utils.readFile import readFile


class FileModal:
    def setupUi(
        self,
        MainWindow,
        closeModal,
        setWindowDimensions,
        getObjectsFromFile,
        saveObjectsToFile,
        window
    ):
        self.closeModal = closeModal
        self.setWindowDimensions = setWindowDimensions
        self.getObjectsFromFile = getObjectsFromFile
        self.saveObjectsToFile = saveObjectsToFile
        self.MainWindow = MainWindow
        self.__window = window

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 350)
        font = QtGui.QFont()
        font.setFamily("Fira Code")
        font.setPointSize(11)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.filesList = QtWidgets.QListWidget(MainWindow)  # may need to create frame
        self.filesList.setGeometry(QtCore.QRect(10, 10, 380, 250))
        self.filesList.setFont(font)
        self.filesList.setObjectName("filesList")
        self.addFilesToList()
        self.filesList.doubleClicked.connect(
            lambda: self.openFile(self.filesList.currentItem().text())
        )

        self.filenameInput = QtWidgets.QLineEdit(MainWindow)
        self.filenameInput.setGeometry(QtCore.QRect(210, 280, 180, 25))
        self.filenameInput.setFont(font)

        self.saveButton = QtWidgets.QPushButton(MainWindow)
        self.saveButton.setGeometry(QtCore.QRect(10, 280, 180, 25))
        self.saveButton.setFont(font)
        self.saveButton.setText("Salvar objeto")
        self.saveButton.clicked.connect(
            lambda: self.saveObjectsToFile(self.filenameInput.text())
        )
        self.saveButton.adjustSize()

    def addFilesToList(self) -> None:
        files = listdir("src/objects")
        files = list(filter((lambda x: ".obj" in x), files))

        for file in files:
            self.filesList.addItem(file)

    def openFile(self, filename: str) -> None:
        objects, window = readFile(filename, self.__window)
        print("IS THIS IT", objects)
        self.getObjectsFromFile(objects)
        self.MainWindow.close()
