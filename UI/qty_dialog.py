from PyQt5 import QtWidgets
from qty import Ui_Form as qty

class QtyDialog(QtWidgets.QDialog, qty):
    def __init__(self, parent=None):
        super().__init__(parent)   
        self.setupUi(self)

        self.pushButton.clicked.connect(self.reject)

        self.pushButton_2.clicked.connect(self.accept)


    def getValue(self):
        return self.doubleSpinBox.value()
