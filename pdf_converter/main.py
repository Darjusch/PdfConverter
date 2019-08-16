
import sys

from PyQt5.uic.Compiler.qtproxies import QtCore
from PySide2.QtWidgets import QApplication, QMainWindow

from pdf_converter.logic.logic import *


class MainWindow(QMainWindow):


    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dict_btn_to_image = {}
        self.pdf_path_list = []
        self.list_of_images = []
        self.list_of_pic_buttons = []

        self.logic = Logic()
        self.ui.open_file_button.clicked.connect(self.setup)

    def setup(self):
        pdf_path = self.logic.select_single_pdf()
        list_of_images = self.logic.pdf_to_jpeg(pdf_path)
        list_of_pic_buttons = self.logic.create_pic_button(list_of_images)
        self.position_pic_buttons_in_grid(list_of_pic_buttons)

    def position_pic_buttons_in_grid(self, list_of_pic_buttons):
        # Todo find a better way to define the ammount of columns
        amount_of_columns = int(len(list_of_pic_buttons) / 2)
        for pic_button in list_of_pic_buttons:
            for x in range(amount_of_columns):
                self.ui.gridLayout.setColumnStretch(x, x + 1)
            self.ui.gridLayout.addWidget(pic_button)
        self.ui.gridLayout(self.ui.gridLayout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

