import copy
import logging
import os
import uuid

from PyPDF2 import PdfFileReader, PdfFileWriter
from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QPushButton
from wand.image import Image as WI

class Logic:

    def create_push_button(self, list_of_pics):
        list_of_push_button = []
        for pic in list_of_pics:
            push_button = QPushButton()
            pixmap = QPixmap(pic)
            button_icon = QIcon(pixmap)
            push_button.setIcon(button_icon)
            push_button.setIconSize(QSize(100, 100))
            push_button.setCheckable(True)
            list_of_push_button.append(push_button)
        return list_of_push_button

    def pdf_to_jpeg(self, pdf_path):
        list_of_images = []
        wand_image_pdf = WI(filename=pdf_path, resolution=20)
        wand_image_jpegs = wand_image_pdf.convert("jpeg")
        for page_number, wand_image_jpeg in enumerate(wand_image_jpegs.sequence):
            jpeg = WI(image=wand_image_jpeg)
            jpeg.save(filename="../output/{0}.jpeg".format(str(page_number)))
            list_of_images.append("../output/{0}.jpeg".format(str(page_number)))
        return list_of_images

    def pdf_splitter(self, path, list_of_push_buttons):
        input = PdfFileReader(open(path, 'rb'))
        n = 0
        name_with_path = os.path.join("../output/" + str(n) + ".pdf")
        n += 1
        output_pdf = open(name_with_path, 'wb')
        output = PdfFileWriter()
        for page_number, pdf_content in enumerate([input.getPage(page) for page in range(0, input.getNumPages())]):
            logging.info('Pagenumber: %s is being processed.', str(page_number))
            if list_of_push_buttons[page_number] in self.checked_buttons(list_of_push_buttons):
                logging.info('Pagenumber: %s is being split.', str(page_number))
                left, right = self.split(pdf_content)
                # In python even numbers are True and odd numbers are False
                if page_number or page_number is 0:
                    output.addPage(left)
                output.addPage(right)
            else:
                output.addPage(pdf_content)
        output.write(output_pdf)
        output_pdf.close()

    def split(self, pdf_content):
        pdf_content_left = copy.copy(pdf_content)
        pdf_content_right = copy.copy(pdf_content)
        (w, h) = pdf_content.mediaBox.upperRight
        pdf_content_left.mediaBox.upperRight = (w / 2, h)
        pdf_content_right.mediaBox.upperLeft = (w / 2, h)
        return pdf_content_left, pdf_content_right

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