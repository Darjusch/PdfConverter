import glob
import sys
import logging
import os
import PyQt5.QtWidgets
import src.Gui.PicButton
import src.Logic.pdfSplitter
import src.Logic.pdfCropper
import src.Tests.testing
from functools import partial
from PyQt5.QtGui import QPixmap
from wand.image import Image as WI


class PdfConverter(PyQt5.QtWidgets.QWidget):
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')

    dict_btn_to_image = {}

    def __init__(self):
        super().__init__()

        self.btn_select_pdf_directory = self.create_btn_with_event('Select pdf Folder',
                                                                   self.pdfs_out_of_selected_directory, 50, 0)
        self.btn_select_pdf_file = self.create_btn_with_event('Select pdf File', self.select_single_pdf, 250, 0)
        # Todo can we just call a Dialog return value with out rerunning the dialog? Fix this
        self.btn_pdf_split = self.create_btn_with_event('Split Pdf', partial(self.split_each_selected_pdf_into_two_pdfs, self.select_single_pdf(), self.checked_buttons(), self.list_of_buttons), 450, 0)
        self.btn_cropper = self.create_btn_with_event('Cropp pdf', pdf_cropper(self), 650, 0)
        self.change_position = self.create_btn_with_event('change_position', self.change_position_of_pic_button, 850, 0)
        self.test = self.create_btn_with_event('test', self.test, 1200, 0)
        self.clear = self.create_btn_with_event('clear', self.clear, 1000, 0)
        self.rotate_button = self.create_btn_with_event('rotate', self.rotate_button, 1300, 0)

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

    def create_btn_with_event(self, label, event, x, y):
        event_button = PyQt5.QtWidgets.QPushButton(label, self)
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
            list_of_pic_buttons.append(pic_button)
            self.dict_btn_to_image[pic_button] = image
        return list_of_pic_buttons

    def pdfs_out_of_selected_directory(self):
        file = str(PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", directory="."))
        pdfs_in_directory = glob.glob(file + '/*.pdf')
        return pdfs_in_directory

    def select_single_pdf(self):
        dialog = PyQt5.QtWidgets.QFileDialog()
        pdf_path = PyQt5.QtWidgets.QFileDialog.getOpenFileName(dialog, "wählen sie x aus", "/", "pdf(*.pdf)")
        return pdf_path[0]

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
                jpeg.save(filename='Output/' + str(page_number) + ".jpeg")
                list_of_images.append('Output/' + str(page_number) + ".jpeg")
                logging.info('Page ' + str(page_number) + ".jpeg" + ' is being converted.')
        return list_of_images

    def position_pic_buttons_in_grid(self, list_of_pic_buttons):
        amount_of_columns = int(len(self.list_of_images) / 2)
        for pic_button in list_of_pic_buttons:
            for x in range(amount_of_columns):
                self.grid_layout.setColumnStretch(x, x + 1)
            self.grid_layout.addWidget(pic_button)
        self.setLayout(self.grid_layout)

    def split_each_selected_pdf_into_two_pdfs(self, pdf_path_list, checked_buttons, list_of_buttons):
        for pdf_path in pdf_path_list:
            pdf_splitter(checked_buttons, pdf_path, list_of_buttons)
            self.clear_memory()
            filename = glob.glob('Output/*.pdf')[0]
            pdf_path_list.append(filename)
            self.pdf_to_jpeg(pdf_path_list)

    def checked_buttons(self, list_of_buttons):
        checked_buttons = []
        for button in list_of_buttons:
            if button.isChecked():
                checked_buttons.append(button)
        return checked_buttons

    # Todo split into two functions one which sends a list of the buttons that has to be swaped and one which does that
    def change_position_of_pic_button(self, list_of_images):
        images_to_be_swaped = []
        for button in self.checked_buttons(self.create_pic_button(list_of_images)):
            image = self.dict_btn_to_image[button]
            images_to_be_swaped.append(image)
        index_one = list_of_images.index(images_to_be_swaped[1])
        index_two = list_of_images.index(images_to_be_swaped[0])
        list_of_images[index_one], list_of_images[index_two] = images_to_be_swaped[0], images_to_be_swaped[1]
        os.rename(list_of_images[index_one], "avoid overwriting.jpeg")
        os.rename(list_of_images[index_two], images_to_be_swaped[1])
        os.rename("avoid overwriting.jpeg", images_to_be_swaped[0])
        self.clear_memory()
        self.position_pic_buttons_in_grid(self.create_pic_button(list_of_images))
        del images_to_be_swaped[:]

    def delete_old_position(self):
        for pic_button in reversed(range(self.grid_layout.count())):
            button_to_remove = self.grid_layout.itemAt(pic_button).widget()
            self.grid_layout.removeWidget(button_to_remove)
            button_to_remove.setParent(None)
            self.list_of_buttons.remove(button_to_remove)
        return self.grid_layout

    def test(self):
        src.Tests.testing.MyTest.pdf_to_jpeg_test(self)
        src.Tests.testing.MyTest.split_each_selected_pdf_into_two_pdfs_test(self)

    def clear_memory(self):
        self.delete_old_position()
        self.dict_btn_to_image.clear()

    def rotate_button(self):
        pass

if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    ex = PdfConverter()
    sys.exit(app.exec_())

# run the application until the user closes it
