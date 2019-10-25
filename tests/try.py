from PySide2.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.button = ''
        btn = QPushButton('Open Second', self)
        btn.move(10, 10)
        btn.clicked.connect(self.openSecond)

        self.resize(420, 450)

        button = QPushButton(self)
        button.move(100,100)
        button.setText("current text")
        self.button = button

    def openSecond(self):
        self.SW = SecondWindow(self.button, parent=self)
        self.SW.show()


class SecondWindow(QMainWindow):
    def __init__(self, button, parent=None):
        super(SecondWindow, self).__init__()
        self.parent = parent
        lbl = QLabel('Second Window', self)
        button.setText("updated text")
        self.parent.buttons = button


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())