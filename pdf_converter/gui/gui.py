from PyQt5 import QtWidgets, uic
import sys

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('pdfConverterDesign2.0.ui', self) # Load the .ui file
        self.open_folder_button = self.findChild(QtWidgets.QToolButton, 'open_folder_button')
        self.open_file_button = self.findChild(QtWidgets.QToolButton, 'open_file_button')
        self.pdf_split_button = self.findChild(QtWidgets.QToolButton, 'pdf_split_button')
        # Todo either give list of buttons or give list of checked buttons
        self.crop_button = self.findChild(QtWidgets.QToolButton, 'crop_button')
        self.change_position_button = self.findChild(QtWidgets.QToolButton, 'change_position_button')
        self.rotate_button = self.findChild(QtWidgets.QToolButton, 'rotate_button')
        self.right_button = self.findChild(QtWidgets.QToolButton, 'right_button')
        self.left_button = self.findChild(QtWidgets.QToolButton, 'left_button')
        self.test_button = self.findChild(QtWidgets.QToolButton, 'test_button')
        self.trash_button = self.findChild(QtWidgets.QToolButton, 'trash_button')
        #self.test_button.clicked.connect(self.printButtonPressed)
        self.show() # Show the GUI

    def printButtonPressed(self):
        print("printButtonPressed")

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
app.exec_() # Start the application
