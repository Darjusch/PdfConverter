from PyPDF2 import PdfFileReader
from src.pdfSplitter import pdf_splitter
from src.main import PdfConverter
import os
import logging


class MyTest():

    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')

    def pdf_to_jpeg_test(self):
        pdf_path_list = ['/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/src/Testing/test.pdf']
        PdfConverter.pdf_to_jpeg(self, pdf_path_list)
        total_number_of_jpegs = 0
        list_of_files = os.listdir('/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/src')
        for file in list_of_files:
            if file.endswith('.jpeg'):
                total_number_of_jpegs += 1
        pdf = PdfFileReader(open('/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/src/Testing/test.pdf', 'rb'))
        if total_number_of_jpegs == pdf.getNumPages():
            logging.info("pdf_to_jpeg_test True")
            return True
        else:
            logging.info("pdf_to_jpeg_test False")
            return False

    def split_each_selected_pdf_into_two_pdfs_test(self):
        pdf_path_list = ['/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/src/Testing/test.pdf']
        checked_buttons = ['False', 'True', 'False', 'True']
        list_of_buttons = ['True', 'True', 'False', 'False', 'True', 'True', 'False', 'False']
        pdf_splitter(pdf_path_list[0], checked_buttons, list_of_buttons)
        total_number_of_jpegs = 0
        list_of_files = os.listdir('/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/src')
        for file in list_of_files:
            if file.endswith('.jpeg'):
                total_number_of_jpegs += 1
        pdf = PdfFileReader(open('/Users/darjusch.schrand/PycharmProjects/PyPdfConverter/src/Testing/test.pdf', 'rb'))
        if total_number_of_jpegs == pdf.getNumPages():
            logging.info("split_each_selected_pdf_into_two_pdfs_test True")
            return True
        else:
            logging.info("split_each_selected_pdf_into_two_pdfs_test False")
            return False
