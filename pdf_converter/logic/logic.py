import copy
import logging
import os
import uuid
from PyPDF2 import PdfFileReader, PdfFileWriter


from wand.image import Image as WI

from pdf_converter.page_object import PageObject


class Logic:

    def pdf_to_push_button(self, pdf_path, resolution=50):
        page_objects = []
        with WI(filename=pdf_path, resolution=resolution) as pdf_img:
            for page in pdf_img.sequence:
                obj = PageObject(page)
                page_objects.append(obj)
        return page_objects


    # Todo: Problem with file saving / replacing.
    def pdf_splitter(self, path, list_of_push_buttons):
        input = PdfFileReader(open(path, 'rb'))
        #os.remove("../output/output.pdf")
        name_with_path = os.path.join("../output/" + str(uuid.uuid4()) + ".pdf")
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
        # Example width of pdf is 500.000
        # Width / 2 = 250.000 -> upperRight is 500.000
        # Width / 2 = 250.000 -> lowerLeft is 0
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


    def cropp_pdf(self):
        pass

    def swipe_right(self):
        pass

    def swipe_left(self):
        pass

    def ui_jpeg_split(self, qimages_to_split):
        split_images = []
        for image_nr, qimg in enumerate(qimages_to_split):
            w, h = qimg.width(), qimg.height()
            qimg_copy = qimg.copy(0, 0, w/2, h)
            split_images.append(qimg_copy)
            qimg_copy2 = qimg.copy(w/2, 0, w/2, h)
            split_images.append(qimg_copy2)
        return split_images


