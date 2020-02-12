import sys
from PySide2.QtWidgets import QInputDialog, QApplication, QLineEdit, QPushButton, QFormLayout, QWidget, QLabel


class inputdialogdemo(QWidget):
    def __init__(self, parent=None):
        super(inputdialogdemo, self).__init__(parent)
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Pixel: ')
        if ok:
            print(str(text))
        self.setWindowTitle("Pdf Cropping")


def main():
    app = QApplication(sys.argv)
    ex = inputdialogdemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()