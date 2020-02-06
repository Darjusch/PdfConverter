#!/usr/bin/env python
import sys

from PySide2.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu


class MyWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MyWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Example MainWindow")
        menu_bar = self.menuBar()  # type: QMenuBar
        file_menu = menu_bar.addMenu("File")  # type: QMenu
        file_menu.addAction("Exit", QApplication.quit)


if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(application.exec_())