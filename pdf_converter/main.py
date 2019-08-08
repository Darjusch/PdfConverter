import glob
import logging
import os
import sys
from functools import partial
from PyQt5 import QtGui, QtCore
import PyQt5.QtWidgets
from PyQt5.QtGui import QPixmap
from wand.image import Image as WI

from pdf_converter.logic.pdf_splitter import pdf_splitter
from tests import testing
from pdf_converter.gui.pic_button import PicButton


class PdfConverter(PyQt5.QtWidgets.QWidget):
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')

    def __init__(self):
        super().__init__()

        self.dict_btn_to_image = {}
        self.pdf_path_list = []
        self.list_of_images = []
        self.list_of_buttons = []

        self.btn_select_pdf_directory = self.create_btn_with_event('Select pdf Folder',
                                                                   self.pdfs_out_of_selected_directory, 'icons/folder.png',50, 0)
        self.btn_select_pdf_file = self.create_btn_with_event('Select pdf File', self.select_single_pdf, 'icons/file.png', 250, 0)
        # Todo can we just call a Dialog return value with out rerunning the dialog? Fix this
        self.btn_pdf_split = self.create_btn_with_event('Split Pdf', partial(self.split_each_selected_pdf_into_two_pdfs, self.pdf_path_list, self.list_of_buttons), 'icons/pdfsplit.png', 450, 0)
        # Todo either give list of buttons or give list of checked buttons
        #self.btn_cropper = self.create_btn_with_event('Cropp pdf', pdf_cropper(self), 650, 0)
        self.change_position = self.create_btn_with_event('change_position', self.change_position_of_pic_button, 'icons/swap.png', 850, 0)
        self.rotate_button = self.create_btn_with_event('rotate', self.rotate_pdf, 'icons/rotate.jpeg', 1000, 0)
        self.test = self.create_btn_with_event('test', self.test, 'icons/test.png', 1200, 0)
        self.clear = self.create_btn_with_event('clear', self.clear_memory, 'icons/trash.jpeg', 1300, 0)

        self.upper_left_new_x_coordinate = self.create_textbox_with_label("upper_left_x_coordinate", 220, 100)
        self.upper_left_new_y_coordinate = self.create_textbox_with_label("upper_left_y_coordinate", 220, 150)
        self.upper_right_new_x_coordinate = self.create_textbox_with_label("upper_right_x_coordinate", 220, 200)
        self.upper_right_new_y_coordinate = self.create_textbox_with_label("upper_right_y_coordinate", 220, 250)
        self.lower_left_new_x_coordinate = self.create_textbox_with_label("lower_left_x_coordinate", 220, 300)
        self.lower_left_new_y_coordinate = self.create_textbox_with_label("lower_left_y_coordinate", 220, 350)
        self.lower_right_new_x_coordinate = self.create_textbox_with_label("lower_right_x_coordinate", 220, 400)
        self.lower_right_new_y_coordinate = self.create_textbox_with_label("lower_right_y_coordinate", 220, 450)
        self.setGeometry(10, 10, 1920, 1080)
        self.grid_layout = PyQt5.QtWidgets.QGridLayout()
        self.show()

    def create_textbox_with_label(self, label_text, x, y):
        textbox = PyQt5.QtWidgets.QLineEdit(self)
        label = PyQt5.QtWidgets.QLabel(self)
        label.setText(label_text)
        label.move(x - 200, y)
        textbox.move(x, y)
        return textbox

    def create_btn_with_event(self, label, event, icon, x, y):
        event_button = PyQt5.QtWidgets.QPushButton(label, self)
        event_button.setIcon(QtGui.QIcon(icon))
        event_button.setIconSize(QtCore.QSize(24,24))
        event_button.clicked.connect(event)
        event_button.move(x, y)
        return event_button

    def create_pic_button(self, list_of_images):
        list_of_pic_buttons = []
        for image in list_of_images:
            pic_button = PicButton(QPixmap(image))
            pic_button.setFixedHeight(200)
            pic_button.setFixedWidth(200)
            pic_button.setCheckable(True)
            # Todo fix dublicated code problem
            list_of_pic_buttons.append(pic_button)
            self.list_of_buttons.append(pic_button)
            self.dict_btn_to_image[pic_button] = image
        self.position_pic_buttons_in_grid(list_of_pic_buttons)
        return list_of_pic_buttons

    def pdfs_out_of_selected_directory(self):
        file = str(PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", directory="."))
        pdfs_in_directory = glob.glob(file + '/*.pdf')
        self.pdf_path_list.append(pdfs_in_directory)
        self.pdf_to_jpeg(pdfs_in_directory)

    def select_single_pdf(self):
        dialog = PyQt5.QtWidgets.QFileDialog()
        pdf_path = PyQt5.QtWidgets.QFileDialog.getOpenFileName(dialog, "wählen sie x aus", "/", "pdf(*.pdf)")
        self.pdf_path_list.append(pdf_path[0])
        self.pdf_to_jpeg([pdf_path[0]])

    '''
    If to slow -> lower resolution
    '''
    def pdf_to_jpeg(self, pdf_path_list):
        list_of_images = []
        for pdf_path in pdf_path_list:
            wand_image_pdf = WI(filename=pdf_path, resolution=20)
            wand_image_jpegs = wand_image_pdf.convert("jpeg")
            for page_number, wand_image_jpeg in enumerate(wand_image_jpegs.sequence):
                jpeg = WI(image=wand_image_jpeg)
                jpeg.save(filename="output/{0}.jpeg".format(str(page_number)))
                list_of_images.append("output/{0}.jpeg".format(str(page_number)))
                # Todo delete duplicated code
                self.list_of_images.append("output/{0}.jpeg".format(str(page_number)))
                logging.info("Page %s.jpeg is being converted.", str(page_number))
        self.create_pic_button(list_of_images)
        return list_of_images

    def position_pic_buttons_in_grid(self, list_of_pic_buttons):
        # Todo find a better way to define the ammount of columns
        amount_of_columns = int(len(list_of_pic_buttons) / 2)
        for pic_button in list_of_pic_buttons:
            for x in range(amount_of_columns):
                self.grid_layout.setColumnStretch(x, x + 1)
            self.grid_layout.addWidget(pic_button)
        self.setLayout(self.grid_layout)

    def split_each_selected_pdf_into_two_pdfs(self, pdf_path_list, list_of_buttons):
        pdf_splitter(pdf_path_list, self.checked_buttons(), list_of_buttons)
        self.clear_memory()
        filename = glob.glob('output/*.pdf')[0]
        pdf_path_list.append(filename)
        self.pdf_to_jpeg(pdf_path_list)

    def checked_buttons(self):
        checked_buttons = []
        for button in self.list_of_buttons:
            if button.isChecked():
                checked_buttons.append(button)
        return checked_buttons

    # Todo split into two functions one which sends a list of the buttons that has to be swaped and one which does that
    # Todo we need a better way of tracking the current state of the buttons.
    def change_position_of_pic_button(self):
        images_to_be_swaped = []
        for button in self.checked_buttons():
            image = self.dict_btn_to_image[button]
            images_to_be_swaped.append(image)
        index_one = self.list_of_images.index(images_to_be_swaped[1])
        index_two = self.list_of_images.index(images_to_be_swaped[0])
        self.list_of_images[index_one], self.list_of_images[index_two] = images_to_be_swaped[0], images_to_be_swaped[1]
        os.rename(self.list_of_images[index_one], "avoid overwriting.jpeg")
        os.rename(self.list_of_images[index_two], images_to_be_swaped[1])
        os.rename("avoid overwriting.jpeg", images_to_be_swaped[0])
        self.clear_memory()
        self.position_pic_buttons_in_grid(self.create_pic_button(self.list_of_images))
        del images_to_be_swaped[:]

    def delete_old_position(self):
        for pic_button in reversed(range(self.grid_layout.count())):
            button_to_remove = self.grid_layout.itemAt(pic_button).widget()
            self.grid_layout.removeWidget(button_to_remove)
            button_to_remove.setParent(None)
            self.list_of_buttons.remove(button_to_remove)
        return self.grid_layout

    def test(self):
        testing.MyTest.pdf_to_jpeg_test(self)
        testing.MyTest.split_each_selected_pdf_into_two_pdfs_test(self)

    def clear_memory(self):
        self.delete_old_position()
        self.dict_btn_to_image.clear()
        self.pdf_path_list.clear()
        self.list_of_images.clear()
        self.list_of_buttons.clear()
        #files = glob.glob('src/output/*')
        #for f in files:
        #    os.remove(f)

    def rotate_pdf(self):

        print("clicked")


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    ex = PdfConverter()
    sys.exit(app.exec_())
