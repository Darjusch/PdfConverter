from PySide2.QtWidgets import QMainWindow, QPushButton, QApplication, QFileDialog, QScrollArea, QGridLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.main_widget = QWidget()
        self.scroll = QScrollArea()
        self.scroll.setWidget(self.main_widget)
        self.grid = QGridLayout(self.main_widget)

        for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            btn = QPushButton(c)
            self.grid.addWidget(btn)

        self.scroll.setFixedHeight(400)
        self.grid.addWidget(self.scroll)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())
