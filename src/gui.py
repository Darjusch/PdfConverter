import glob
import sys
import time
import logging

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from wand.image import Image as wi

from src.main.PicButton import PicButton
from src.pdfConverter import pdfSplitter


class PdfConverter(QWidget):
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')

    '''
    Initializing the buttons and defining what happens on click event.
    '''
    def __init__(self):
        super().__init__()

        self.btnSelectPdfDirectory = self.create_btn_with_event('Select pdf Folder', self.on_select_pdf_directory, 50, 0)
        self.btnSelectPdfFile = self.create_btn_with_event('Select pdf File', self.on_select_pdf_file, 250, 0)
        self.btnPdf2Jpeg = self.create_btn_with_event('Pdf2Jpeg', self.pdf2jpeg, 450, 0)
        self.btnPdfSplit = self.create_btn_with_event('Split Pdf', self.on_split_pdf, 650, 0)
        self.setGeometry(10, 10, 920, 720)
        self.show()

    '''
    Creates Button 
    '''
    def create_btn_with_event(self, label, event, x, y):
        btn = QPushButton(label, self)
        btn.clicked.connect(event)
        btn.move(x, y)
        return btn

    pdfPathList = []
    directoryPath = []

    '''
    Filters all pdfs out of selected Folder
    '''
    def on_select_pdf_directory(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory", directory="."))
        self.directoryPath.append(file)
        folderContent = glob.glob(file + '/*.pdf')
        for pdfPath in folderContent:
            self.pdfPathList.append(pdfPath)

    '''
    Select a pdf File
    '''
    def on_select_pdf_file(self):
        dialog = QFileDialog()
        path = QFileDialog.getOpenFileName(dialog, "wählen sie x aus", "/", "pdf(*.pdf)")
        self.pdfPathList.append(path[0])

    '''
    Calls the function to split the pdfs.
    '''
    def on_split_pdf(self):
        start = time.time()
        pageNumber = 1
        for pdf in self.pdfPathList:
            pdfSplitter(pdf, pageNumber)
            pageNumber += 1
        end = time.time()
        runtime = end - start
        logging.info('Function on_split_pdf(+ pdfSplitter) take(s): ' + str(runtime) + ' seconds!')

    '''
    Converts the pdf's to jpeg's.
    '''
    def pdf2jpeg(self):
        start = time.time()
        for pdfName in self.pdfPathList:
            pdf = wi(filename=pdfName, resolution=20)
            pdfImage = pdf.convert("jpeg")
            i = 1
            listImages = []
            for img in pdfImage.sequence:
                page = wi(image=img)
                page.save(filename=str(i) + ".jpeg")
                listImages.append(str(i) + ".jpeg")
                i += 1
                logging.info('Page ' + str(i) + ".jpeg" + ' is being processed.')
            self.setLayout(self.populate_grid(listImages))
            end = time.time()
            runtime = end - start
            logging.info('Function pdf2jpeg(+ populate_grid) take(s): ' + str(runtime) + ' seconds!')

    '''
    Displays each pdf as an Image
    '''
    def populate_grid(self, images):
        grid_layout = QGridLayout()
        every_four_images = len(images) / 3
        for img in images:
            for x in range(int(every_four_images)):
                grid_layout.setColumnStretch(x, x + 1)
            button = PicButton(QPixmap(img).scaled(180, 180))
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
