from PySide2.QtWidgets import QMainWindow, QPushButton, QApplication, QFileDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.button = ''
        btn = QPushButton('Open File', self)
        btn.move(10, 10)
        btn.clicked.connect(self.open_file)
        self.resize(420, 450)

    def open_file(self):
        pdf_dialog_obj = QFileDialog.getOpenFileNames(self, "Open Pdf", "/Downloads", "Pdf Files (*.pdf)",)
        pdf_path = pdf_dialog_obj[0]
        print(pdf_path)

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())
