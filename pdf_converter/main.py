import copy
import sys
import glob
import os
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
        self.list_of_push_buttons = []
        self.logic = Logic()
        self.ui.openFileButton.clicked.connect(self.setup)
        self.ui.splitButton.clicked.connect(self.split_pdfs)
        self.ui.changePositionOfPicButton.clicked.connect(partial(self.change_position_of_pic_button, self.list_of_push_buttons))
        self.ui.rotateButton.clicked.connect(Logic.rotate_pdf)
        self.ui.cropButton.clicked.connect(Logic.cropp_pdf)
        # clear memory or delete old position?
        self.ui.trashButton.clicked.connect(self.delete_old_position)
        self.ui.leftButton.clicked.connect(Logic.swipe_left)
        self.ui.rightButton.clicked.connect(Logic.swipe_right)

    # Todo self is from Logic not from main
    def setup(self):
        self.list_of_images = self.logic.pdf_to_jpeg(self.pdf_path_list[0])
        list_of_push_buttons, dict_btn_to_image = self.logic.create_push_button(self.list_of_images)
        self.dict_btn_to_image = dict_btn_to_image.copy()
        for button in list_of_push_buttons:
            self.list_of_push_buttons.append(button)
        grid = self.position_push_buttons_in_grid(list_of_push_buttons)
        self.ui.widgetLayout.setLayout(grid)


    def split_pdfs(self):
        self.logic.split_each_selected_pdf_into_two_pdfs(self.pdf_path_list[0], self.list_of_push_buttons)
        self.clear_memory()
        filename = glob.glob('../output/*.pdf')[0]
        self.pdf_path_list.append(filename)
        self.setup()

    def position_push_buttons_in_grid(self, list_of_push_buttons):
        row = 0
        column = 0
        for push_button in list_of_push_buttons:
            self.ui.pushButtonGrid.addWidget(push_button, row, column)
            column += 1
            if int(len(list_of_push_buttons) / 2) is column:
                row += 1
                column = 0
        return self.ui.pushButtonGrid

    def delete_old_position(self):
        for push_button in reversed(range(self.ui.pushButtonGrid.count())):
            button_to_remove = self.ui.pushButtonGrid.itemAt(push_button).widget()
            self.ui.pushButtonGrid.removeWidget(button_to_remove)
            button_to_remove.setParent(None)
            self.list_of_push_buttons.remove(button_to_remove)
        return self.ui.pushButtonGrid


    #Todo problem with self -> Is from logic not MainWindow
    def clear_memory(self):
        self.delete_old_position()
        self.dict_btn_to_image.clear()
        self.pdf_path_list.clear()
        self.list_of_images.clear()
        self.list_of_push_buttons.clear()
        #files = glob.glob('../output/*')
        #for f in files:
        #    os.remove(f)

    # Todo split into two functions one which sends a list of the buttons that has to be swaped and one which does that
    def change_position_of_pic_button(self, list_of_push_buttons):
        images_to_be_swaped = []
        for button in self.logic.checked_buttons(list_of_push_buttons):
            image = self.dict_btn_to_image[button]
            images_to_be_swaped.append(image)
        index_one = self.list_of_images.index(images_to_be_swaped[1])
        index_two = self.list_of_images.index(images_to_be_swaped[0])
        self.list_of_images[index_one], self.list_of_images[index_two] = images_to_be_swaped[0], \
                                                                                     images_to_be_swaped[1]
        os.rename(self.list_of_images[index_one], "../output/avoid overwriting.jpeg")
        os.rename(self.list_of_images[index_two], images_to_be_swaped[1])
        os.rename("../output/avoid overwriting.jpeg", images_to_be_swaped[0])
        self.clear_memory()
        grid = self.position_push_buttons_in_grid(list_of_push_buttons)
        self.ui.widgetLayout.setLayout(grid)
        del images_to_be_swaped[:]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
