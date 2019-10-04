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
        self.pdf_path_list = ["../tests/test2.pdf"]
        self.list_of_images = []
        self.push_button_to_image = {}
        self.logic = Logic()
        self.ui.openFileButton.clicked.connect(partial(self.setup, self.pdf_path_list))
        self.ui.splitButton.clicked.connect(self.split_pdfs_ui)
        self.ui.changePositionOfPicButton.clicked.connect(partial(self.change_position_of_pic_button,
                                                                  self.push_button_to_image))
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
        images_to_split = []
        checked_buttons = self.logic.checked_buttons(self.push_button_to_image)
        for button in checked_buttons:
            images_to_split.append(self.push_button_to_image[button])
            del self.push_button_to_image[button]
        split_images = self.logic.ui_jpeg_split(images_to_split)
        new_push_buttons_to_images = self.logic.create_push_button(split_images)
        self.push_button_to_image.update(new_push_buttons_to_images)
        self.delete_old_position()
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
            if int(len(list_of_push_buttons) / 4) is column:
                row += 1
                column = 0
        self.ui.widgetLayout.setLayout(self.ui.pushButtonGrid)

    def delete_old_position(self):
        for push_button in reversed(range(self.ui.pushButtonGrid.count())):
            button_to_remove = self.ui.pushButtonGrid.itemAt(push_button).widget()
            self.ui.pushButtonGrid.removeWidget(button_to_remove)
            button_to_remove.setParent(None)
        return self.ui.pushButtonGrid

    def change_position_of_pic_button(self, list_of_push_buttons1):
        button_to_switch = []
        for button in self.push_button_to_image.keys():
            if button.isChecked():
                button_to_switch.append(button)
        self.push_button_to_image[button_to_switch[0]], self.push_button_to_image[button_to_switch[1]] = \
            self.push_button_to_image[button_to_switch[1]], self.push_button_to_image[button_to_switch[0]]
        self.delete_old_position()
        self.position_push_buttons_in_grid(self.push_button_to_image.keys())
        del button_to_switch[:]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
