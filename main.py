from PyQt5.QtWidgets import QApplication
import sys
from src.View.View import View

if (__name__ == "__main__"):
    app = QApplication(sys.argv)
    view = View()
    view.show()
    sys.exit(app.exec_())