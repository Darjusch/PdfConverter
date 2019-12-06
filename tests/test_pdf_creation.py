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

    def test_adjusting_of_coordinates(self):
        self.pdf_creator.adjust_coordinates_of_output_pdf_to_edited_pdf()
        output_coordinates = [
            self.pdf_creator.output_lower_left_x,
            self.pdf_creator.output_lower_left_y,
            self.pdf_creator.output_upper_right_x,
            self.pdf_creator.output_upper_right_y
        ]
        expected_coordinates = [0, 0, 1062, 892]
        self.assertListEqual(output_coordinates, expected_coordinates)


if __name__ == '__main__':
    unittest.main()
