import sys
import glob
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
        self.pdf_path_list = ["../tests/test2.pdf"]
        self.qimages = []
        self.page_objects = []
        self.logic = Logic()
        self.ui.openFileButton.clicked.connect(partial(self.setup, self.pdf_path_list))
        self.ui.splitButton.clicked.connect(self.split_pdfs_ui)
        self.ui.changePositionOfPicButton.clicked.connect(self.change_position_of_pic_button)
        self.ui.rotateButton.clicked.connect(self.rotate_pdf_ui)
        self.ui.cropButton.clicked.connect(Logic.cropp_pdf)
        self.ui.trashButton.clicked.connect(self.delete_old_position)
        self.ui.leftButton.clicked.connect(Logic.swipe_left)
        self.ui.rightButton.clicked.connect(Logic.swipe_right)
        self.ui.testButton.clicked.connect(Logic.ui_jpeg_split)

    def setup(self, pdf):
        self.page_objects.clear()
        self.page_objects = self.logic.pdf_to_push_button(pdf[0])
        self.position_push_buttons_in_grid()

    def split_pdfs_ui(self):
        for index, object in enumerate(self.page_objects):
            if object.push_button.isChecked():
                second_object = copy.copy(object)
                object.splitLeft()
                second_object.splitRight()
                self.page_objects.insert(index+1, second_object)
        self.delete_old_position()
        self.position_push_buttons_in_grid()


    def split_pdfs(self):
        self.logic.pdf_splitter(self.pdf_path_list[0], self.page_objects.keys())
        filename = glob.glob('../output/*.pdf')[0]
        self.delete_old_position()
        self.pdf_path_list.clear()
        self.qimages.clear()
        self.page_objects.clear()
        self.page_objects = self.logic.pdf_to_push_button(filename)
        self.position_push_buttons_in_grid()
        self.pdf_path_list.append(filename)

    def position_push_buttons_in_grid(self):
        row = 0
        column = 0
        for page_object in self.page_objects:
            self.ui.pushButtonGrid.addWidget(page_object.push_button, row, column)
            column += 1
            if int(len(self.page_objects) / 4) is column:
                row += 1
                column = 0
        self.ui.widgetLayout.setLayout(self.ui.pushButtonGrid)

    def delete_old_position(self):
        for push_button in reversed(range(self.ui.pushButtonGrid.count())):
            button_to_remove = self.ui.pushButtonGrid.itemAt(push_button).widget()
            self.ui.pushButtonGrid.removeWidget(button_to_remove)
            button_to_remove.setParent(None)
        return self.ui.pushButtonGrid

    def change_position_of_pic_button(self):
        checked = []
        for index, object in enumerate(self.page_objects):
            if object.push_button.isChecked():
                checked.append(object)
        if len(checked) is not 2:
            return
        index1 = self.page_objects.index(checked[0])
        index2 = self.page_objects.index(checked[1])
        self.page_objects[index1] = checked[1]
        self.page_objects[index2] = checked[0]
        self.delete_old_position()
        self.position_push_buttons_in_grid()

    def rotate_pdf(self):
        checked_buttons = self.logic.checked_buttons(list(self.page_objects.keys()))
        pdf = open("../tests/test2.pdf", 'rb')
        pdf_reader = PdfFileReader(pdf)
        pdf_writer = PdfFileWriter()
        for page_number in range(pdf_reader.numPages):
            if list(self.page_objects.keys())[page_number] in checked_buttons:
                page = pdf_reader.getPage(page_number)
                page.rotateClockwise(90)
                pdf_writer.addPage(page)
            else:
                pdf_writer.addPage(pdf_reader.getPage(page_number))
        output = open("../output/rotated_pdf", 'wb')
        pdf_writer.write(output)
        pdf.close()
        output.close()
        self.page_objects = self.logic.pdf_to_push_button("../output/rotated_pdf")
        self.delete_old_position()
        self.position_push_buttons_in_grid()

    def rotate_pdf_ui(self):
        for index, object in enumerate(self.page_objects):
            if object.push_button.isChecked():
                object.img.rotate(90)
                object.rotation += 90
        self.delete_old_position()
        self.position_push_buttons_in_grid()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
