from src.PicButton import *
import glob
import sys
import logging
from PIL import Image
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from wand.image import Image as wi
from src.pdfSplitter import pdf_splitter
from PyPDF2 import PdfFileWriter, PdfFileReader


class PdfConverter(QWidget):
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')

    pdf_path_list = []
    directory_path = []
    list_of_buttons = []
    list_of_images = []
    dict_btn_to_image = {}

    def __init__(self):
        super().__init__()

        self.btn_select_pdf_directory = self.create_btn_with_event('Select pdf Folder',
                                                                   self.pdfs_out_of_selected_directory, 50, 0)
        self.btn_select_pdf_file = self.create_btn_with_event('Select pdf File', self.select_pdf, 250, 0)
        self.btn_pdf_split = self.create_btn_with_event('Split Pdf', self.split_each_selected_pdf_into_two_pdfs, 450, 0)
        self.btn_cropper = self.create_btn_with_event('Cropp pdf', self.pdf_cropper, 650, 0)
        self.change_position = self.create_btn_with_event('change_position', self.change_position_of_pic_button, 850, 0)
        self.setGeometry(10, 10, 1920, 1080)
        self.grid_layout = QGridLayout()

        self.show()

    def create_btn_with_event(self, label, event, x, y):
        btn = QPushButton(label, self)
        btn.clicked.connect(event)
        btn.move(x, y)
        return btn

    def pdfs_out_of_selected_directory(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory", directory="."))
        self.directory_path.append(file)
        pdfs_in_directory = glob.glob(file + '/*.pdf')
        [self.pdf_path_list.append(pdf_path) for pdf_path in pdfs_in_directory]
        self.pdf_2_jpeg()

    def select_pdf(self):
        dialog = QFileDialog()
        pdf_path = QFileDialog.getOpenFileName(dialog, "wählen sie x aus", "/", "pdf(*.pdf)")
        self.pdf_path_list.append(pdf_path[0])
        self.pdf_2_jpeg()

    '''
    If to slow -> lower resolution
    '''
    def pdf_2_jpeg(self):
        for pdf_path in self.pdf_path_list:
            wand_image_pdf = wi(filename=pdf_path, resolution=20)
            wand_image_jpegs = wand_image_pdf.convert("jpeg")
            for page_number, wand_image_jpeg in enumerate(wand_image_jpegs.sequence):
                jpeg = wi(image=wand_image_jpeg)
                jpeg.save(filename=str(page_number) + ".jpeg")
                self.list_of_images.append(str(page_number) + ".jpeg")
                logging.info('Page ' + str(page_number) + ".jpeg" + ' is being converted.')
        self.setLayout(self.position_pic_btns_in_grid())

    def position_pic_btns_in_grid(self):
        amount_of_columns = int(len(self.list_of_images) / 2)
        for image in self.list_of_images:
            for x in range(amount_of_columns):
                self.grid_layout.setColumnStretch(x, x + 1)
            self.grid_layout.addWidget(self.create_pic_button(image))
        return self.grid_layout

    def create_pic_button(self, image):
        button = PicButton(QPixmap(image))
        button.setFixedHeight(200)
        button.setFixedWidth(200)
        button.setCheckable(True)
        self.list_of_buttons.append(button)
        self.dict_btn_to_image[button] = image
        return button

    # Todo multiple pdf input doesnt work yet
    # Todo diplay in gui

    def split_each_selected_pdf_into_two_pdfs(self):
        for pdf_path in self.pdf_path_list:
            pdf_splitter(self.checked_buttons(), pdf_path, self.list_of_buttons)

    def checked_buttons(self):
        checked_buttons = []
        for button in self.list_of_buttons:
            if button.isChecked():
                checked_buttons.append(button)
        return checked_buttons

    # Todo take user input
    def pdf_cropper(self):
        for button in self.checked_buttons():
            if button.isChecked():
                file = PdfFileReader(open("KW22_Version_A_mOeffnungszeiten_2505-3105 Kopie 2.pdf", "rb"))
                page = file.getPage(0)
                lower_right_new_x_coordinate = 611
                lower_right_new_y_coordinate = 500
                lower_left_new_x_coordinate = 0
                lower_left_new_y_coordinate = 500
                upper_right_new_x_coordinate = 611
                upper_right_new_y_coordinate = 700
                upper_left_new_x_coordinate = 0
                upper_left_new_y_coordinate = 700
                page.mediaBox.lowerRight = (lower_right_new_x_coordinate, lower_right_new_y_coordinate)
                page.mediaBox.lowerLeft = (lower_left_new_x_coordinate, lower_left_new_y_coordinate)
                page.mediaBox.upperRight = (upper_right_new_x_coordinate, upper_right_new_y_coordinate)
                page.mediaBox.upperLeft = (upper_left_new_x_coordinate, upper_left_new_y_coordinate)
                output = PdfFileWriter()
                output.addPage(page)
                output.write(open("cropped.pdf", "wb"))

    # Todo function to change position of elements
    def change_position_of_pic_button(self):
        images_to_be_swaped = []
        for button in self.checked_buttons():
            image = self.dict_btn_to_image[button]
            images_to_be_swaped.append(image)
        index_one = self.list_of_images.index(images_to_be_swaped[1])
        index_two = self.list_of_images.index(images_to_be_swaped[0])
        self.list_of_images[index_one], self.list_of_images[index_two] = images_to_be_swaped[0], images_to_be_swaped[1]
        self.delete_old_position()
        self.position_pic_btns_in_grid()

    def delete_old_position(self):
        for i in reversed(range(self.grid_layout.count())):
            button_to_remove = self.grid_layout.itemAt(i).widget()
            self.grid_layout.removeWidget(button_to_remove)
            button_to_remove.setParent(None)
        return self.grid_layout


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PdfConverter()
    sys.exit(app.exec_())

# run the application until the user closes it
