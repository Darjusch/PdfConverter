import copy
import sys
from functools import partial

from PyPDF2 import PdfFileReader

from pdf_converter.gui.crop_pagewindow import PdfPageWindow
from pdf_converter.gui.ui_mainwindow import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from wand.image import Image as WandImage

from pdf_converter.logic.logic import Logic
from pdf_converter.page_object import PageObject


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.logic = Logic()
        self.page_objects = []
        self.checked_objects = []
        self.pdf_path = ''
        self.pdf_reader = None
        self.page_window = None
        self.button_to_remove = None
        self.row = 0
        self.column = 0
        self.ui.openFileButton.clicked.connect(self.dialog_to_select_pdfs)
        self.ui.openFolderButton.clicked.connect(self.dialog_to_select_folder_with_pdfs)
        self.ui.splitButton.clicked.connect(partial(self.ui_action_handler, 'split'))
        self.ui.changePositionOfObjects.clicked.connect(partial(self.ui_action_handler, 'change_position'))
        self.ui.rotateLeftButton.clicked.connect(partial(self.ui_action_handler, 'rotate', -90))
        self.ui.rotateRightButton.clicked.connect(partial(self.ui_action_handler, 'rotate', 90))
        self.ui.cropButton.clicked.connect(self.open_checked_pdf_page_in_new_window)
        self.ui.trashButton.clicked.connect(partial(self.ui_action_handler, 'delete'))
        self.ui.resetButton.clicked.connect(self.get_position_from_push_button_in_grid)
        self.ui.createPdfButton.clicked.connect(self.send_data_for_creating_pdf)

    def open_checked_pdf_page_in_new_window(self):
        self.is_push_button_checked()
        if len(self.checked_objects) is 1:
            self.page_window = PdfPageWindow(self.checked_objects[0], parent=self)
            self.page_window.show()

    def dialog_to_select_pdfs(self):
        pdf_dialog_obj = QFileDialog.getOpenFileNames(self, "Open Pdf", "/Downloads", "Pdf Files (*.pdf)",)
        self.pdf_path = pdf_dialog_obj[0][0]
        self.setup()

    def dialog_to_select_folder_with_pdfs(self):
        path = QFileDialog.getExistingDirectory()
        pass

    def setup(self):
        self.page_objects.clear()
        self.open_and_read_pdf()
        self.position_push_button_in_grid()

    def open_and_read_pdf(self):
        pdf_file_obj = open(self.pdf_path, 'rb')
        self.pdf_reader = PdfFileReader(pdf_file_obj)
        self.convert_pdf_pages_to_push_button()

    def convert_pdf_pages_to_push_button(self, resolution=25):
        with WandImage(filename=self.pdf_path, resolution=resolution) as pdf_img:
            for index, wi_page in enumerate(pdf_img.sequence):
                self.create_page_objects(index, wi_page)

    def create_page_objects(self, index, wi_page):
        obj = PageObject(wi_page, self.pdf_reader.getPage(index))
        self.page_objects.append(obj)

    def ui_action_handler(self, action, degree=0):
        self.is_push_button_checked()
        if action == 'change_position' and len(self.checked_objects) is 2:
            self.change_position_of_objects_ui()
        else:
            for obj in self.checked_objects:
                if action == 'delete':
                    self.page_objects.remove(obj)
                elif action == 'rotate':
                    self.rotate_push_button_ui(obj, degree)
                elif action == 'split':
                    self.split_push_button_ui(obj)
        self.deleted_old_and_position_new_push_button_in_grid()

    def is_push_button_checked(self):
        self.checked_objects = []
        for index, object in enumerate(self.page_objects):
            if object.push_button.isChecked():
                self.checked_objects.append(object)

    def change_position_of_objects_ui(self):
        self.page_objects[0], self.page_objects[1] = self.checked_objects[1], self.checked_objects[0]

    def rotate_push_button_ui(self, obj, degree):
        obj.rotate_image_update_rotation_and_push_button(degree)
        obj.rotation += degree

    def split_push_button_ui(self, object):
        copy_of_object = copy.copy(object)
        object.split_left()
        copy_of_object.split_right()
        self.page_objects.insert(self.page_objects.index(object) + 1, copy_of_object)

    def deleted_old_and_position_new_push_button_in_grid(self):
        self.get_position_from_push_button_in_grid()

    def get_position_from_push_button_in_grid(self):
        for push_button in reversed(range(self.ui.pushButtonGrid.count())):
            self.button_to_remove = self.ui.pushButtonGrid.itemAt(push_button).widget()
            self.delete_push_button_from_grid()

    def delete_push_button_from_grid(self):
        self.ui.pushButtonGrid.removeWidget(self.button_to_remove)
        self.button_to_remove.setParent(None)
        self.reset_grid_rows_and_columns()

    def reset_grid_rows_and_columns(self):
        self.row = 0
        self.column = 0
        self.position_push_button_in_grid()

    def position_push_button_in_grid(self):
        for page_object in self.page_objects:
            self.position_push_button_in_grid_row(page_object.push_button)
            if int(len(self.page_objects) / 4) is self.column:
                self.create_new_grid_row()
        self.ui.widgetLayout.setLayout(self.ui.pushButtonGrid)

    def position_push_button_in_grid_row(self, push_button):
        self.ui.pushButtonGrid.addWidget(push_button, self.row, self.column)
        self.column += 1

    def create_new_grid_row(self):
        self.row += 1
        self.column = 0

    def send_data_for_creating_pdf(self):
        self.logic.create_pdf_action_handler(self.page_objects)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
