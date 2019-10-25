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
        self.page_objects = self.main.pdf_to_push_button("../tests/test2.pdf")
        self.page_object = self.page_objects[0]
        self.img = self.page_object.img
        self.rotation = self.page_object.rotation
        self.page = self.page_object.pdf_page

    def test_image_is_QImage(self):
        self.assertIsInstance(self.img, PySide2.QtGui.QImage)

    def test_page_converts_to_image(self):
        self.assertIsInstance(self.page_object.pageToImage(self.page_object.pdf_page), PySide2.QtGui.QImage)

    def test_pdf_to_push_button_len(self):
        self.assertEqual(len(self.page_objects), 12)

    def test_pdf_roates_left(self):
        self.page_object.rotate(-90)
        self.assertEqual(self.page_object.rotation, -90)

    def test_pdf_rotates_right(self):
        self.page_object.rotate(90)
        self.assertEqual(self.page_object.rotation, 90)

    def test_split_pdf_left(self):
        original_page = self.page_object.pdf_page
        self.page_object.splitLeft()
        after_split_page = self.page_object.pdf_page
        self.assertEqual(after_split_page, original_page)

    def test_split_pdf_right(self):
        original_page = self.page_object.pdf_page
        self.page_object.splitRight()
        after_split_page = self.page_object.pdf_page
        self.assertEqual(after_split_page, original_page)

    def test_convert_coordinates(self):
        self.page_object.convert_coordinates(50, 50, 100, 100)
        self.assertAlmostEqual(self.page_object.x1, 0.25)


if __name__ == '__main__':
    unittest.main()
