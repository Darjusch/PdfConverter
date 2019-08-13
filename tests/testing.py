from PyPDF2 import PdfFileReader
from pdf_converter.main import *
import os
import logging
import logging.config


class MyTest():
    logging.config.fileConfig(fname='logging.config', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    def pdf_to_jpeg_test(self):
        pdf_path_list = ['tests/test.pdf']
        PdfConverter.pdf_to_jpeg(self, pdf_path_list)
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
