import sys
from functools import partial
from pdf_converter.gui.ui_mainwindow import Ui_MainWindow
sys.path.append('..')
from PySide2.QtWidgets import QApplication, QMainWindow
from pdf_converter.logic.logic import *


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.page_objects = []
        self.logic = Logic()
        self.ui.openFileButton.clicked.connect(partial(self.setup, "../tests/test2.pdf"))
        self.ui.splitButton.clicked.connect(partial(self.ui_action_handler, 'split'))
        self.ui.changePositionOfObjects.clicked.connect(partial(self.ui_action_handler, 'change_position'))
        self.ui.rotateLeftButton.clicked.connect(partial(self.ui_action_handler, 'rotate_left'))
        self.ui.rotateRightButton.clicked.connect(partial(self.ui_action_handler, 'rotate_right'))
        self.ui.cropButton.clicked.connect(Logic.cropp_pdf)
        self.ui.trashButton.clicked.connect(partial(self.ui_action_handler, 'delete'))
        self.ui.leftButton.clicked.connect(Logic.swipe_left)
        self.ui.rightButton.clicked.connect(Logic.swipe_right)
        self.ui.resetButton.clicked.connect(self.delete_push_button_from_grid)

    def setup(self, pdf):
        self.page_objects.clear()
        self.page_objects = self.logic.pdf_to_push_button(pdf)
        self.position_push_button_in_grid()

    def ui_action_handler(self, action):
        checked_objects = self.is_object_checked()
        if action == 'change_position' and len(checked_objects) is 2:
            self.change_position_of_objects_ui(checked_objects)
        for index, obj in enumerate(checked_objects):
            if action == 'delete':
                self.page_objects.remove(obj)
            elif action == 'rotate_right':
                self.rotate_pdf_ui(obj, 90)
            elif action == 'rotate_left':
                self.rotate_pdf_ui(obj, -90)
            elif action == 'split':
                self.split_pdf_ui(obj, index)
        self.delete_push_button_from_grid()
        self.position_push_button_in_grid()

    def is_object_checked(self):
        checked_objects = []
        for index, object in enumerate(self.page_objects):
            if object.push_button.isChecked():
                checked_objects.append(object)
        return checked_objects

    def change_position_of_objects_ui(self, checked_objects):
        index1, index2 = self.page_objects.index(checked_objects[0]), self.page_objects.index(checked_objects[1])
        self.page_objects[index1], self.page_objects[index2] = checked_objects[1], checked_objects[0]

    def rotate_pdf_ui(self, obj, degree):
        obj.rotate(degree)
        obj.rotation += degree

    def split_pdf_ui(self, obj, index):
        second_obj = copy.copy(obj)
        obj.splitLeft()
        second_obj.splitRight()
        self.page_objects.insert(index+1, second_obj)

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
