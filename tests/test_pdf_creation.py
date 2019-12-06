import copy
import sys
import unittest

from PySide2.QtWidgets import QApplication

from pdf_converter.logic.pdf_creation import PdfCreator
from pdf_converter.main import MainWindow

app = QApplication(sys.argv)


class TestPdfCreation(unittest.TestCase):

    def setUp(self):
        self.main = MainWindow()
        self.main.pdf_path = "../tests/test2.pdf"
        self.main.open_and_read_pdf()
        self.pdf_creator = PdfCreator()
        self.pdf_creator.page_object = self.main.page_objects[0]
        self.page_object = self.main.page_objects[0]
        self.pdf_creator.page = self.page_object.page

    def test_create_copy_of_page(self):
        page_copy = copy.copy(self.page_object.page)
        self.pdf_creator.create_copy_of_page()
        self.assertEquals(type(self.pdf_creator.page), type(page_copy))


if __name__ == '__main__':
    unittest.main()
