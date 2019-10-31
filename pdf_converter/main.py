import copy
import sys
from functools import partial
from pdf_converter.gui.pdf_pagewindow import PdfPageWindow
from pdf_converter.gui.ui_mainwindow import Ui_MainWindow
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from wand.image import Image as WI
from pdf_converter.page_object import PageObject


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.page_objects = []
        self.ui.openFileButton.clicked.connect(self.dialog_to_select_pdfs)
        self.ui.openFolderButton.clicked.connect(self.dialog_to_select_folder_with_pdfs)
        self.ui.splitButton.clicked.connect(partial(self.ui_action_handler, 'split'))
        self.ui.changePositionOfObjects.clicked.connect(partial(self.ui_action_handler, 'change_position'))
        self.ui.rotateLeftButton.clicked.connect(partial(self.ui_action_handler, 'rotate_left'))
        self.ui.rotateRightButton.clicked.connect(partial(self.ui_action_handler, 'rotate_right'))
        self.ui.cropButton.clicked.connect(self.open_checked_pdf_page_in_new_window)
        self.ui.trashButton.clicked.connect(partial(self.ui_action_handler, 'delete'))
        self.ui.resetButton.clicked.connect(self.delete_push_button_from_grid)

    def open_checked_pdf_page_in_new_window(self):
        if len(self.is_push_button_checked()) is 1:
            checked_object = self.is_push_button_checked()[0]
            self.page_window = PdfPageWindow(checked_object, parent=self)
            self.page_window.show()

    def dialog_to_select_pdfs(self):
        pdf_dialog_obj = QFileDialog.getOpenFileNames(self, "Open Pdf", "/Downloads", "Pdf Files (*.pdf)",)
        pdf = pdf_dialog_obj[0][0]
        self.setup(pdf)

    def dialog_to_select_folder_with_pdfs(self):
        path = QFileDialog.getExistingDirectory()
        pass

    def setup(self, pdf):
        self.page_objects.clear()
        self.page_objects = self.convert_pdf_pages_to_push_button(pdf)
        self.position_push_button_in_grid()

    def convert_pdf_pages_to_push_button(self, pdf_path, resolution=25):
        page_objects = []
        with WI(filename=pdf_path, resolution=resolution) as pdf_img:
            for page in pdf_img.sequence:
                obj = PageObject(page)
                page_objects.append(obj)
        return page_objects

    def ui_action_handler(self, action):
        checked_objects = self.is_push_button_checked()
        if action == 'change_position' and len(checked_objects) is 2:
            self.change_position_of_objects_ui(checked_objects)
        for obj in checked_objects:
            if action == 'delete':
                self.page_objects.remove(obj)
            elif action == 'rotate_right':
                self.rotate_push_button_ui(obj, 90)
            elif action == 'rotate_left':
                self.rotate_push_button_ui(obj, -90)
            elif action == 'split':
                self.split_push_button_ui(obj)
        self.delete_push_button_from_grid()
        self.position_push_button_in_grid()

    def is_push_button_checked(self):
        checked_objects = []
        for index, object in enumerate(self.page_objects):
            if object.push_button.isChecked():
                checked_objects.append(object)
        return checked_objects

    def change_position_of_objects_ui(self, checked_objects):
        index1, index2 = self.page_objects.index(checked_objects[0]), self.page_objects.index(checked_objects[1])
        self.page_objects[index1], self.page_objects[index2] = checked_objects[1], checked_objects[0]

    def rotate_push_button_ui(self, obj, degree):
        obj.rotate(degree)
        obj.rotation += degree

    def split_push_button_ui(self, obj):
        second_obj = copy.copy(obj)
        obj.split_left()
        second_obj.split_right()
        self.page_objects.insert(self.page_objects.index(obj)+1, second_obj)

    def delete_push_button_from_grid(self):
        for push_button in reversed(range(self.ui.pushButtonGrid.count())):
            button_to_remove = self.ui.pushButtonGrid.itemAt(push_button).widget()
            self.ui.pushButtonGrid.removeWidget(button_to_remove)
            button_to_remove.setParent(None)
        return self.ui.pushButtonGrid

    def position_push_button_in_grid(self):
        row = 0
        column = 0
        for page_object in self.page_objects:
            self.ui.pushButtonGrid.addWidget(page_object.push_button, row, column)
            column += 1
            if int(len(self.page_objects) / 4) is column:
                row += 1
                column = 0
        self.ui.widgetLayout.setLayout(self.ui.pushButtonGrid)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
