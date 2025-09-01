from UI.main_UI import Mainapp
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Mainapp()
    window.show()
    sys.exit(app.exec_())