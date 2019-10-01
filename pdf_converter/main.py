import sys
import glob
from functools import partial
from pdf_converter.gui.ui_mainwindow import Ui_MainWindow
sys.path.append('..')
from PySide2.QtWidgets import QApplication, QMainWindow
from pdf_converter.logic.logic import *


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.dict_btn_to_image = {}
        self.pdf_path_list = ["../tests/test2.pdf"]
        self.list_of_images = []
        self.push_button_to_image = {}
        self.logic = Logic()
        self.ui.openFileButton.clicked.connect(partial(self.setup, self.pdf_path_list))
        self.ui.splitButton.clicked.connect(self.split_pdfs_ui)
        self.ui.changePositionOfPicButton.clicked.connect(partial(self.change_position_of_pic_button,
                                                                  self.push_button_to_image.keys()))
        self.ui.rotateButton.clicked.connect(Logic.rotate_pdf)
        self.ui.cropButton.clicked.connect(Logic.cropp_pdf)
        self.ui.trashButton.clicked.connect(self.delete_old_position)
        self.ui.leftButton.clicked.connect(Logic.swipe_left)
        self.ui.rightButton.clicked.connect(Logic.swipe_right)
        self.ui.testButton.clicked.connect(Logic.ui_jpeg_split)

    def setup(self, pdf):
        self.list_of_images = self.logic.pdf_to_jpeg(pdf[0])
        self.push_button_to_image.clear()
        self.push_button_to_image = self.logic.create_push_button(self.list_of_images)
        self.position_push_buttons_in_grid(self.push_button_to_image.keys())

    def split_pdfs_ui(self):
        list_of_images = self.logic.ui_jpeg_split(self.push_button_to_image)
        self.push_button_to_image = self.logic.create_push_button(list_of_images)
        self.position_push_buttons_in_grid(self.push_button_to_image.keys())


    def split_pdfs(self):
        self.logic.pdf_splitter(self.pdf_path_list[0], self.push_button_to_image.keys())
        filename = glob.glob('../output/*.pdf')[0]
        self.delete_old_position()
        self.pdf_path_list.clear()
        self.list_of_images.clear()
        self.push_button_to_image.clear()
        self.push_button_to_image = self.logic.create_push_button(self.logic.pdf_to_jpeg(filename))
        self.position_push_buttons_in_grid(self.push_button_to_image.keys())
        self.pdf_path_list.append(filename)

    def position_push_buttons_in_grid(self, list_of_push_buttons):
        row = 0
        column = 0
        for push_button in list_of_push_buttons:
            self.ui.pushButtonGrid.addWidget(push_button, row, column)
            column += 1
            if int(len(list_of_push_buttons) / 3) is column:
                row += 1
                column = 0
        self.ui.widgetLayout.setLayout(self.ui.pushButtonGrid)

    def delete_old_position(self):
        for push_button in reversed(range(self.ui.pushButtonGrid.count())):
            button_to_remove = self.ui.pushButtonGrid.itemAt(push_button).widget()
            self.ui.pushButtonGrid.removeWidget(button_to_remove)
            button_to_remove.setParent(None)
        return self.ui.pushButtonGrid

    def change_position_of_pic_button(self, list_of_push_buttons):
        list_of_indexes = []
        for button in list_of_push_buttons:
            if button.isChecked():
                list_of_indexes.append(list_of_push_buttons.index(button))
        self.delete_old_position()
        list_of_push_buttons[list_of_indexes[0]], list_of_push_buttons[list_of_indexes[1]] = \
            list_of_push_buttons[list_of_indexes[1]], list_of_push_buttons[list_of_indexes[0]]
        self.position_push_buttons_in_grid(list_of_push_buttons)
        del list_of_indexes[:]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
