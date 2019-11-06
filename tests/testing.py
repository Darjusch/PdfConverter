import PySide2
import sys
from PySide2.QtGui import QImage
from PySide2.QtWidgets import QApplication
from pdf_converter.main import MainWindow
import unittest
app = QApplication(sys.argv)


class PageObjectTest(unittest.TestCase):

    def setUp(self):
        self.main = MainWindow()
        self.page_objects = self.main.convert_pdf_pages_to_push_button("../tests/test2.pdf")
        self.page_object = self.page_objects[0]
        self.img = self.page_object.img
        self.rotation = self.page_object.rotation
        self.page = self.page_object.pdf_page

    def test_if_page_converts_to_qimage(self):
        self.assertIsInstance(self.page_object.page_to_qimage(self.page_object.pdf_page), PySide2.QtGui.QImage)

    def test_if_len_pdf_pages_equals_created_push_button(self):
        self.assertEqual(len(self.page_objects), 4)

    def test_if_pdf_rotates_left(self):
        self.page_object.rotate(-90)
        self.assertEqual(self.page_object.rotation, -90)

    def test_if_pdf_rotates_right(self):
        self.page_object.rotate(90)
        self.assertEqual(self.page_object.rotation, 90)

    def test_split_left_side_of_pdf_page(self):
        original_page = self.page_object.pdf_page
        self.page_object.split_left()
        after_split_page = self.page_object.pdf_page
        self.assertEqual(after_split_page, original_page)

    def test_split_right_side_of_pdf_page(self):
        original_page = self.page_object.pdf_page
        self.page_object.split_right()
        after_split_page = self.page_object.pdf_page
        self.assertEqual(after_split_page, original_page)

    def test_convert_coordinates_into_percentage(self):
        self.page_object.convert_coordinates_into_percentage(50, 50, 100, 100)
        self.assertListEqual(
            [
                round(self.page_object.x1, 3),
                round(self.page_object.y1, 3),
                round(self.page_object.x2, 3),
                round(self.page_object.y2, 3)
            ],
            [0.136, 0.161, 0.407, 0.484]
        )


if __name__ == '__main__':
    unittest.main()
