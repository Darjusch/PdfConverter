import copy
import logging
import os
import uuid
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtWidgets import QPushButton
from wand.image import Image as WI


class Logic:

    def create_push_button(self, list_of_pics):
        push_button_to_image = {}
        for pic in list_of_pics:
            push_button = QPushButton()
            pixmap = QPixmap(pic)
            button_icon = QIcon(pixmap)
            push_button.setIcon(button_icon)
            push_button.setIconSize(QSize(100, 100))
            push_button.setCheckable(True)
            push_button_to_image[push_button] = pic
        return push_button_to_image

    def pdf_to_jpeg(self, pdf_path):
        list_of_images = []
        wand_image_pdf = WI(filename=pdf_path, resolution=20)
        wand_image_jpegs = wand_image_pdf.convert("jpeg")
        for page_number, wand_image_jpeg in enumerate(wand_image_jpegs.sequence):
            jpeg = WI(image=wand_image_jpeg)
            jpeg.save(filename="../output/{0}.jpeg".format(str(page_number)))
            list_of_images.append("../output/{0}.jpeg".format(str(page_number)))
        return list_of_images

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

    def ui_jpeg_split(self, images_to_split):
        split_images = []
        for image_nr, image in enumerate(images_to_split):
            img = Image.open(image)
            img_width, img_height = img.size
            box = (0, 0, img_width/2, img_height)
            image1 = img.crop(box)
            image1.save("../output/split1" + str(image_nr) + ".jpeg")
            box = (img_width/2, 0, img_width, img_height)
            image2 = img.crop(box)
            image2.save("../output/split2" + str(image_nr) + ".jpeg")
            split_images.append("../output/split1" + str(image_nr) +".jpeg")
            split_images.append("../output/split2" + str(image_nr) + ".jpeg")
        return split_images

