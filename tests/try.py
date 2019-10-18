from PySide2.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        btn = QPushButton('Open Second', self)
        btn.move(10, 10)
        btn.clicked.connect(self.openSecond)

        btn2 = QPushButton('Open Third', self)
        btn2.move(110, 10)
        btn2.clicked.connect(self.openThird)

        self.resize(220, 50)

    def openSecond(self):
        self.SW = SecondWindow()
        self.SW.show()

    def openThird(self):
        self.TW = ThirdWindow()
        self.TW.show()

class SecondWindow(QMainWindow):
    def __init__(self):
        super(SecondWindow, self).__init__()
        lbl = QLabel('Second Window', self)

class ThirdWindow(QMainWindow):
    def __init__(self):
        super(ThirdWindow, self).__init__()
        lbl = QLabel('Third Window', self)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())