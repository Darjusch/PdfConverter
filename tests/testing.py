from PyPDF2 import PdfFileReader
from pdf_converter.main import *
import os
import logging


class MyTest():

    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')

    def pdf_to_jpeg_test(self):
        pdf_path_list = ['/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/tests/test.pdf']
        PdfConverter.pdf_to_jpeg(self, pdf_path_list)
        total_number_of_jpegs = 0
        list_of_files = os.listdir('/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/output')
        for file in list_of_files:
            if file.endswith('.jpeg'):
                total_number_of_jpegs += 1
        pdf = PdfFileReader(open('/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/tests/test.pdf', 'rb'))
        logging.info("number of jpegs: %s number of pages: %s", str(total_number_of_jpegs), str(pdf.getNumPages()))
        if total_number_of_jpegs == pdf.getNumPages():
            logging.info("pdf_to_jpeg_test True")
            return True
        else:
            logging.info("pdf_to_jpeg_test False")
            return False

    def split_each_selected_pdf_into_two_pdfs_test(self):
        pdf_path_list = ['/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/tests/test.pdf']
        checked_buttons = ['False', 'True', 'False', 'True']
        list_of_buttons = ['True', 'True', 'False', 'False', 'True', 'True', 'False', 'False']
        pdf_splitter(pdf_path_list, checked_buttons, list_of_buttons)
        total_number_of_jpegs = 0
        list_of_files = os.listdir('/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/output')
        for file in list_of_files:
            if file.endswith('.jpeg'):
                total_number_of_jpegs += 1
        pdf = PdfFileReader(open('/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/tests/test.pdf', 'rb'))
        logging.info("number of jpegs: %s number of pages: %s", str(total_number_of_jpegs), str(pdf.getNumPages()))
        if total_number_of_jpegs == pdf.getNumPages():
            logging.info("split_each_selected_pdf_into_two_pdfs_test True")
            return True
        else:
            logging.info("split_each_selected_pdf_into_two_pdfs_test False")
            return False

