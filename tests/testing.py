import unittest
import logging.config
from pdf_converter.logic.logic import *

class MyTest(unittest.TestCase):


    def pdf_to_jpeg_test(self):
        pdf_path_list = ['tests/test.pdf']
        #self.assertEquals(Logic.pdf_to_jpeg(pdf_path_list), list_of_images)
        total_number_of_jpegs = 0
        list_of_files = os.listdir('output')
        for file in list_of_files:
            if file.endswith('.jpeg'):
                total_number_of_jpegs += 1
        pdf = PdfFileReader(open('tests/test.pdf', 'rb'))
        if total_number_of_jpegs == pdf.getNumPages():
            logging.info("pdf_to_jpeg_test True")
            return True
        else:
            logging.info("pdf_to_jpeg_test False")
            return False

    def split_each_selected_pdf_into_two_pdfs_test(self):
        pdf_path_list = ['tests/test.pdf']
        checked_buttons = ['False', 'True', 'False', 'True']
        list_of_buttons = ['True', 'True', 'False', 'False', 'True', 'True', 'False', 'False']
        pdf_splitter(pdf_path_list, checked_buttons, list_of_buttons)
        total_number_of_jpegs = 0
        list_of_files = os.listdir('output')
        for file in list_of_files:
            if file.endswith('.jpeg'):
                total_number_of_jpegs += 1
        pdf = PdfFileReader(open('tests/test.pdf', 'rb'))
        if total_number_of_jpegs == pdf.getNumPages():
            logging.info("split_each_selected_pdf_into_two_pdfs_test True")
            return True
        else:
            logging.info("split_each_selected_pdf_into_two_pdfs_test False")
            return False
