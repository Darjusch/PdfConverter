import sys
from PySide2.QtWidgets import QApplication
from pdf_converter.gui.ui_mainwindow import Ui_MainWindow
from pdf_converter.main import MainWindow
import unittest

app = QApplication(sys.argv)


class TestMainWindow(unittest.TestCase):

    def setUp(self):
        self.main = MainWindow()
        self.main.pdf_path = "../tests/test2.pdf"
        self.main.open_and_read_pdf()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main)
        self.main.page_objects[0].push_button.setChecked(True)
        self.main.page_objects[1].push_button.setChecked(True)
        self.main.is_push_button_checked()

    def test_change_position_of_objects(self):
        page_objects_copy = self.main.page_objects.copy()
        self.main.change_position_of_objects_ui()
        self.assertListEqual([page_objects_copy[0], page_objects_copy[1]], [self.main.page_objects[1], self.main.page_objects[0]])

    def test_if_push_button_are_checked(self):
        self.main.is_push_button_checked()
        self.assertEqual(len(self.main.checked_objects), 2)

    def test_action_handler_delete_single_page(self):
        page_objects_copy = self.main.page_objects.copy()
        self.main.page_objects[0].push_button.setChecked(True)
        self.main.page_objects[1].push_button.setChecked(False)
        self.main.ui_action_handler('delete')
        self.assertEqual(len(page_objects_copy)-1, len(self.main.page_objects))

    def test_action_handler_delete_multiple_pages(self):
        page_objects_copy = self.main.page_objects.copy()
        self.main.page_objects[0].push_button.setChecked(False)
        self.main.page_objects[1].push_button.setChecked(True)
        self.main.page_objects[2].push_button.setChecked(True)
        self.main.ui_action_handler('delete')
        self.assertEqual(len(page_objects_copy)-2, len(self.main.page_objects))

    def test_position_push_button_in_grid(self):
        self.main.position_push_button_in_grid()
        push_button_in_grid = self.main.ui.pushButtonGrid.count()
        self.assertEqual(push_button_in_grid, 4)

    def test_delete_push_button_from_grid(self):
        self.main.position_push_button_in_grid()
        if self.ui.pushButtonGrid.count() == 4:
            self.main.page_objects[1].push_button.setChecked(True)
            self.main.ui_action_handler('delete')
            self.main.get_position_from_push_button_in_grid()
            self.assertEqual(self.ui.pushButtonGrid.count(), 3)
        else:
            print("Position_push_button_didnt_work")

if __name__ == '__main__':
    unittest.main()