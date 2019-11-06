from pytestqt.plugin import qtbot

from pdf_converter.gui.ui_mainwindow import Ui_MainWindow
from pdf_converter.main import MainWindow


class Ui_Testing(qtbot):

    def setUp(self):
        self.main = MainWindow()
        self.main.page_objects = self.main.convert_pdf_pages_to_push_button("../tests/test2.pdf")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main)

    def test_starting(self, qtbot):
        pass