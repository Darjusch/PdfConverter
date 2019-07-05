from src.PicButton import *
import glob
import sys
import time
import logging
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from wand.image import Image as wi

from src.pdfSplitter import pdf_splitter


class PdfConverter(QWidget):
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')

    '''
    Initializing the buttons and defining what happens on click event.
    '''
    def __init__(self):
        super().__init__()

        self.btn_select_pdf_directory = self.create_btn_with_event('Select pdf Folder', self.on_select_pdf_directory, 50, 0)
        self.btn_select_pdf_file = self.create_btn_with_event('Select pdf File', self.on_select_pdf_file, 250, 0)
        self.btn_pdf_2_jpeg = self.create_btn_with_event('Pdf2Jpeg', self.pdf2jpeg, 450, 0)
        self.btn_pdf_split = self.create_btn_with_event('Split Pdf', self.on_split_pdf, 650, 0)
        self.setGeometry(10, 10, 1920, 1080)
        self.show()

    '''
    Creates Button with events
    Input -> str, function(), int, int
    Output -> button object
    '''
    def create_btn_with_event(self, label, event, x, y):
        btn = QPushButton(label, self)
        btn.clicked.connect(event)
        btn.move(x, y)
        return btn

    pdf_path_list = []
    directory_path = []

    '''
    Allows user to select a folder -> filters all Pdf(s) out of the selected Folder
    '''
    def on_select_pdf_directory(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory", directory="."))
        self.directory_path.append(file)
        folder_content = glob.glob(file + '/*.pdf')
        [self.pdf_path_list.append(pdf_path) for pdf_path in folder_content]

    '''
    Select a pdf File
    '''
    def on_select_pdf_file(self):
        dialog = QFileDialog()
        path = QFileDialog.getOpenFileName(dialog, "wählen sie x aus", "/", "pdf(*.pdf)")
        self.pdf_path_list.append(path[0])

    '''
    Splits the Pdf(s).
    '''
    def on_split_pdf(self):
        start = time.time()
        [pdf_splitter(page_number, pdf_path) for page_number, pdf_path in enumerate(self.pdf_path_list)]
        end = time.time()
        runtime = end - start
        logging.info('Function on_split_pdf(+ pdfSplitter) take(s): ' + str(runtime) + ' second(s)!')

    '''
    Converts the Pdf(s) to Jpeg(s).
    Lower resolution -> faster output
    '''
    def pdf2jpeg(self):
        start = time.time()
        for pdf_path in self.pdf_path_list:
            list_of_images = []
            pdf = wi(filename=pdf_path, resolution=20)
            pdf_image = pdf.convert("jpeg")
            for index, img in enumerate(pdf_image.sequence):
                page = wi(image=img)
                page.save(filename=str(index) + ".jpeg")
                list_of_images.append(str(index) + ".jpeg")
                logging.info('Page ' + str(index) + ".jpeg" + ' is being processed.')
            self.setLayout(self.populate_grid(list_of_images))
            end = time.time()
            runtime = end - start
            logging.info('Function pdf2jpeg(+ populate_grid) take(s): ' + str(runtime) + ' second(s)!')


    '''
    Displays each pdf as an Image and takes care of the positioning inside the GridLayout
    Turns each Image into a button
    Increase / Decrease the amount of columns by changing the divider of the listOfImages 
    -> (int(len(listOfImages) / divider))
    '''
    def populate_grid(self, list_of_images):
        grid_layout = QGridLayout()
        amount_of_columns = int(len(list_of_images) / 2)
        for img in list_of_images:
            [grid_layout.setColumnStretch(x, x + 1) for x in range(amount_of_columns)]
            button = PicButton(QPixmap(img))
            button.setFixedHeight(200)
            button.setFixedWidth(200)
            button.clicked.connect(self.on_split_pdf)
            grid_layout.addWidget(button)
            logging.info('Image turned to button: ' + img + ".")
        return grid_layout


    # Todo function to merge pdfs
    # Todo function to rotate pdfs


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PdfConverter()
    sys.exit(app.exec_())


# run the application until the user closes it
