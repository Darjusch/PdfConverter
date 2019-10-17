import PySide2
import sys

from PySide2.QtGui import QImage
from PySide2.QtWidgets import QApplication

sys.path.append('..')
from pdf_converter.logic.logic import Logic
import unittest

app = QApplication(sys.argv)


class PageObjectTest(unittest.TestCase):

    def setUp(self):
        self.logic = Logic()
        self.page_objects = self.logic.pdf_to_push_button("../tests/test2.pdf")
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

if __name__ == '__main__':
    unittest.main()
