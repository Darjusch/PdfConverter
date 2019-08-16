import os

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap

from pdf_converter.gui.pic_button import PicButton
import PyQt5.QtWidgets
import glob
from wand.image import Image as WI
import logging
import tests.testing
from pdf_converter.gui.ui_mainwindow import Ui_MainWindow

from pdf_converter.logic.pdf_splitter import pdf_splitter
from pdf_converter.main import MainWindow


class Logic():

    def __init__(self):
        self.ui = Ui_MainWindow()


    def create_pic_button(self, list_of_images):
        list_of_pic_buttons = []
        for image in list_of_images:
            pic_button = PicButton(QPixmap(image))
            pic_button.setFixedHeight(200)
            pic_button.setFixedWidth(200)
            pic_button.setCheckable(True)
            list_of_pic_buttons.append(pic_button)
        return list_of_pic_buttons
            # Todo dict problem.
            #self.MainWindow.dict_btn_to_image[pic_button] = image
        #self.position_pic_buttons_in_grid(list_of_pic_buttons)


    #def pdfs_out_of_selected_directory(self):
    #    file = str(PyQt5.QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory", directory="."))
    #    pdfs_in_directory = glob.glob(file + '/*.pdf')
    #    return pdfs_in_directory


    def select_single_pdf(self):
        dialog = PyQt5.QtWidgets.QFileDialog()
        pdf_path = PyQt5.QtWidgets.QFileDialog.getOpenFileName(dialog, "wählen sie x aus", "/", "pdf(*.pdf)")
        return [pdf_path[0]]

    '''
    If to slow -> lower resolution
    '''
    # Todo split into two functions one that calls pdf_to_jpeg and then calls create_pic_button with the return value
    def pdf_to_jpeg(self, pdf_path_list):
        list_of_images = []
        for pdf_path in pdf_path_list:
            wand_image_pdf = WI(filename=pdf_path, resolution=20)
            wand_image_jpegs = wand_image_pdf.convert("jpeg")
            for page_number, wand_image_jpeg in enumerate(wand_image_jpegs.sequence):
                jpeg = WI(image=wand_image_jpeg)
                jpeg.save(filename="../output/{0}.jpeg".format(str(page_number)))
                list_of_images.append("output/{0}.jpeg".format(str(page_number)))
                #logging.info("Page %s.jpeg is being converted.".format(str(page_number)))
        return list_of_images



    #def split_each_selected_pdf_into_two_pdfs(self, pdf_path_list, list_of_buttons):
    #    pdf_splitter(pdf_path_list, self.checked_buttons(), list_of_buttons)
        #self.clear_memory()
    #    filename = glob.glob('output/*.pdf')[0]
    #    pdf_path_list.append(filename)
    #    self.pdf_to_jpeg_to_pic_button_caller(pdf_path_list)

    #def checked_buttons(self):
    #    checked_buttons = []
    #    for button in MainWindow.list_of_buttons:
    #        if button.isChecked():
    #            checked_buttons.append(button)
    #    return checked_buttons

    # Todo split into two functions one which sends a list of the buttons that has to be swaped and one which does that
    # Todo we need a better way of tracking the current state of the buttons.
    #def change_position_of_pic_button(self):
    #    images_to_be_swaped = []
    #    for button in self.checked_buttons():
    #        image = MainWindow.dict_btn_to_image[button]
    #        images_to_be_swaped.append(image)
    #    index_one = MainWindow.list_of_images.index(images_to_be_swaped[1])
    #    index_two = MainWindow.list_of_images.index(images_to_be_swaped[0])
    #    MainWindow.list_of_images[index_one], MainWindow.list_of_images[index_two] = images_to_be_swaped[0], \
    #                                                                     images_to_be_swaped[1]
    #    os.rename(MainWindow.list_of_images[index_one], "avoid overwriting.jpeg")
    #    os.rename(MainWindow.list_of_images[index_two], images_to_be_swaped[1])
    #    os.rename("avoid overwriting.jpeg", images_to_be_swaped[0])
    #    self.clear_memory()
        #self.position_pic_buttons_in_grid(list_of_pic_button)
    #    del images_to_be_swaped[:]

    #def delete_old_position(self):
    #    for pic_button in reversed(range(self.ui.gridLayout.count())):
    #        button_to_remove = self.ui.gridLayout.itemAt(pic_button).widget()
    #        self.ui.gridLayout.removeWidget(button_to_remove)
    #        button_to_remove.setParent(None)
    #        MainWindow.list_of_buttons.remove(button_to_remove)
    #    return self.ui.gridLayout

    #def test(self):
    #    tests.testing.MyTest.pdf_to_jpeg_test(self)
    #    tests.testing.MyTest.split_each_selected_pdf_into_two_pdfs_test(self)

    #def clear_memory(self):
    #    self.delete_old_position()
    #    MainWindow.dict_btn_to_image.clear()
    #    MainWindow.pdf_path_list.clear()
    #    MainWindow.list_of_images.clear()
    #    MainWindow.list_of_buttons.clear()
        # files = glob.glob('output/*')
        # for f in files:
        #    os.remove(f)

    #def rotate_pdf(self):
    #    pass