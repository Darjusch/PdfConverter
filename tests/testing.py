import sys

sys.path.append('..')
from pdf_converter.logic.logic import Logic
from pyside2uic.properties import QtGui
import unittest


class PageObjectTest(unittest.TestCase):

    def setUp(self):
        self.logic = Logic()
        self.page_objects = self.logic.pdf_to_push_button("../tests/test2.pdf")
        self.page_object = self.page_objects[0]
        self.img = self.page_object.img
        self.rotation = self.page_object.rotation
        self.page = self.page_object.pdf_page

    def test_image_is_QImage(self):
        self.assertIsInstance(type(QtGui.QImage), type(self.img))

    def test_page_is_wand_sequence(self):
        self.assertIsInstance(type(self.page), type('wand.sequence.SingleImage'))

    def test_page_converts_to_image(self):
        self.assertIsInstance(type(self.page_object.pageToimage(self.page_object.pdf_page)), type(QtGui.QImage))

    def test_pdf_to_push_button_len(self):
        self.assertEqual(len(self.page_objects), 12)


if __name__ == '__main__':
    unittest.main()
