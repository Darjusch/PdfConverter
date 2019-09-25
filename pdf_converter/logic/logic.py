from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QPushButton
from wand.image import Image as WI
from pdf_converter.logic.pdf_splitter import pdf_splitter


class Logic:

    def create_push_button(self, list_of_pics):
        list_of_push_button = []
        dict_btn_to_image = {}
        for pic in list_of_pics:
            push_button = QPushButton()
            pixmap = QPixmap(pic)
            button_icon = QIcon(pixmap)
            push_button.setIcon(button_icon)
            push_button.setIconSize(QSize(100, 100))
            push_button.setCheckable(True)
            list_of_push_button.append(push_button)
            dict_btn_to_image[push_button] = pic
        return list_of_push_button, dict_btn_to_image

    def pdf_to_jpeg(self, pdf_path):
        list_of_images = []
        wand_image_pdf = WI(filename=pdf_path, resolution=20)
        wand_image_jpegs = wand_image_pdf.convert("jpeg")
        for page_number, wand_image_jpeg in enumerate(wand_image_jpegs.sequence):
            jpeg = WI(image=wand_image_jpeg)
            jpeg.save(filename="../output/{0}.jpeg".format(str(page_number)))
            list_of_images.append("../output/{0}.jpeg".format(str(page_number)))
        return list_of_images


    def split_each_selected_pdf_into_two_pdfs(self, pdf_path_list, list_of_push_buttons):
        pdf_splitter(pdf_path_list, self.checked_buttons(list_of_push_buttons), list_of_push_buttons)


    def checked_buttons(self, list_of_push_buttons):
        checked_buttons = []
        for button in list_of_push_buttons:
            if button.isChecked():
                checked_buttons.append(button)
        return checked_buttons

    def rotate_pdf(self):
        pass

    def cropp_pdf(self):
        pass

    def swipe_right(self):
        pass

    def swipe_left(self):
        pass