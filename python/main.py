import copy
import os
import sys
from functools import partial

from PyPDF2 import PdfFileReader

from python.gui.ui_mainwindow import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QInputDialog, QLineEdit
from wand.image import Image as WandImage

from python.logic.pdf_creation import PdfCreator
from python.page_object import PageObject


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.logic = PdfCreator()
        self.page_objects = []
        self.checked_objects = []
        page_objects = self.page_objects[:]
        self.manipulation_tracker = [page_objects]
        self.pdf_path = ''
        self.pdf_reader = None
        self.page_window = None
        self.button_to_remove = None
        self.row = 0
        self.column = 0
        self.visible_from = 0
        self.visible_until = 15
        self.current_position = -1
        self.ui.openFileButton.clicked.connect(self.dialog_to_select_pdfs)
        self.ui.openFolderButton.clicked.connect(self.dialog_to_select_folder_with_pdfs)
        self.ui.splitButton.clicked.connect(partial(self.ui_action_handler, 'split'))
        self.ui.changePositionOfObjects.clicked.connect(partial(self.ui_action_handler, 'change_position'))
        self.ui.rotateLeftButton.clicked.connect(partial(self.ui_action_handler, 'rotate', -90))
        self.ui.rotateRightButton.clicked.connect(partial(self.ui_action_handler, 'rotate', 90))
        self.ui.cropButton.clicked.connect(self.open_checked_pdf_page_in_new_window)
        self.ui.trashButton.clicked.connect(partial(self.ui_action_handler, 'delete'))
        self.ui.resetButton.clicked.connect(self.reset)
        self.ui.createPdfButton.clicked.connect(self.send_data_for_creating_pdf)
        self.ui.rightButton.clicked.connect(partial(self.update_visible_button, "+"))
        self.ui.leftButton.clicked.connect(partial(self.update_visible_button, "-"))
        self.ui.undoManipulationButton.clicked.connect(partial(self.re_or_undo_manipulation, -1))
        self.ui.redoManipulationButton.clicked.connect(partial(self.re_or_undo_manipulation, +1))
        self.ui.actionOpen_Output.triggered.connect(self.open_outputfolder)
        self.ui.trippleSplittButton.clicked.connect(partial(self.ui_action_handler, 'tripple_split'))

    def open_checked_pdf_page_in_new_window(self):
        self.is_push_button_checked()
        if len(self.checked_objects) is 1:
            pixel, ok = QInputDialog().getText(self, "QInputDialog().getText()",
                                                 "Pixel to crop:", QLineEdit.Normal)
            self.checked_objects[0].cropp(int(pixel))
            self.deleted_old_and_position_new_push_button_in_grid()

    def dialog_to_select_pdfs(self):
        pdf_dialog_obj = QFileDialog.getOpenFileNames(self, "Open Pdf", "/Downloads", "Pdf Files (*.pdf)",)
        self.pdf_path = pdf_dialog_obj[0][0]
        self.open_and_read_pdf()
        self.position_push_button_in_grid()

    def update_visible_button(self, symbol):
        if symbol is "+" and self.visible_until < len(self.page_objects):
            self.visible_from += 15
            self.visible_until += 15
            self.deleted_old_and_position_new_push_button_in_grid()
        elif symbol is "-" and self.visible_from is not 0:
                self.visible_from -= 15
                self.visible_until -= 15
                self.deleted_old_and_position_new_push_button_in_grid()

    def reset(self):
        self.page_objects.clear()
        self.get_position_from_push_button_in_grid()

    def dialog_to_select_folder_with_pdfs(self):
        path = QFileDialog.getExistingDirectory()
        pdf_pathes = os.listdir(path)[1::]
        for pdf in pdf_pathes:
            self.pdf_path = f"{path}/{pdf}"
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
        page_objects = self.page_objects[:]
        self.manipulation_tracker.append(page_objects)

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
                elif action == 'tripple_split':
                    self.tripple_split_ui(obj)
        page_objects = self.page_objects[:]
        self.manipulation_tracker.append(page_objects)
        self.deleted_old_and_position_new_push_button_in_grid()

    def is_push_button_checked(self):
        self.checked_objects = []
        for index, object in enumerate(self.page_objects):
            if object.push_button.isChecked():
                self.checked_objects.append(object)

    def change_position_of_objects_ui(self):
        first_checked_button, second_checked_button = self.page_objects.index(self.checked_objects[0]), self.page_objects.index(self.checked_objects[1])
        self.page_objects[first_checked_button], self.page_objects[second_checked_button] = self.checked_objects[1], self.checked_objects[0]

    def rotate_push_button_ui(self, obj, degree):
        copy_object = copy.copy(obj)
        copy_object.rotate_image_update_rotation_and_push_button(degree)
        copy_object.rotation += degree
        self.page_objects.insert(self.page_objects.index(obj), copy_object)
        self.page_objects.remove(obj)

    def split_push_button_ui(self, obj):
        first_copy_of_object = copy.copy(obj)
        second_copy_of_object = copy.copy(obj)
        first_copy_of_object.split_left()
        second_copy_of_object.split_right()
        self.page_objects.insert(self.page_objects.index(obj) + 1, second_copy_of_object)
        self.page_objects.insert(self.page_objects.index(obj), first_copy_of_object)
        self.page_objects.remove(obj)

    def tripple_split_ui(self, obj):
        first_copy_of_object = copy.copy(obj)
        second_copy_of_object = copy.copy(obj)
        third_copy_of_object = copy.copy(obj)
        first_copy_of_object.split_first_third()
        second_copy_of_object.split_second_third()
        third_copy_of_object.split_third_third()
        self.page_objects.insert(self.page_objects.index(obj) + 2, third_copy_of_object)
        self.page_objects.insert(self.page_objects.index(obj) + 1, second_copy_of_object)
        self.page_objects.insert(self.page_objects.index(obj), first_copy_of_object)
        self.page_objects.remove(obj)

    def deleted_old_and_position_new_push_button_in_grid(self):
        self.get_position_from_push_button_in_grid()

    def get_position_from_push_button_in_grid(self):
        for push_button in reversed(range(self.ui.pushButtonGrid.count())):
            self.button_to_remove = self.ui.pushButtonGrid.itemAt(push_button).widget()
            self.delete_push_button_from_grid()
        self.reset_grid_rows_and_columns()

    def delete_push_button_from_grid(self):
        self.ui.pushButtonGrid.removeWidget(self.button_to_remove)
        self.button_to_remove.setParent(None)

    def reset_grid_rows_and_columns(self):
        self.row = 0
        self.column = 0
        self.position_push_button_in_grid()

    def position_push_button_in_grid(self):
        for page_object in self.page_objects[self.visible_from:self.visible_until]:
            self.position_push_button_in_grid_row_and_moves_to_next_column(page_object.push_button)
            if 7 is self.column:
                self.create_new_grid_row_and_sets_column_position_to_zero()
        self.ui.widgetLayout.setLayout(self.ui.pushButtonGrid)

    def position_push_button_in_grid_row_and_moves_to_next_column(self, push_button):
        self.ui.pushButtonGrid.addWidget(push_button, self.row, self.column)
        self.column += 1

    def create_new_grid_row_and_sets_column_position_to_zero(self):
        self.row += 1
        self.column = 0

    def send_data_for_creating_pdf(self):
        self.logic.create_pdf_action_handler(self.page_objects)

    def re_or_undo_manipulation(self, change):
        self.current_position = self.current_position + change
        self.page_objects = self.manipulation_tracker[self.current_position]
        self.deleted_old_and_position_new_push_button_in_grid()

    def open_outputfolder(self):
        outputfolder_dialog = QFileDialog.getOpenFileNames(self, 'Your output Pdf', 'Output-folder', 'pdf(*)')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
