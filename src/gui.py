import sys, glob
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from src.pdfConverter import pdfSplitter
from wand.image import Image as wi

class PdfConverter(QWidget):
    '''
    Initializing the buttons and defining what happens on click event.
    '''
    def __init__(self):
        super().__init__()

        self.btnSelectPdfDirectory = self.createBtnWithEvent('Select pdf Folder', self.on_select_pdf_directory, 250, 0)
        self.btnSelectPdfFile = self.createBtnWithEvent('Select pdf File', self.on_select_pdf_file, 250, 50)
        self.btnPdf2Jpeg = self.createBtnWithEvent('Pdf2Jpeg', self.pdf2jpeg, 250, 100)
        self.btnPdfSplit = self.createBtnWithEvent('Split Pdf', self.on_split_pdf, 250, 150)
        self.setGeometry(10, 10, 640, 480)
        self.show()

    def createBtnWithEvent(self, label, event, x, y):
        btn = QPushButton(label, self)
        btn.clicked.connect(event)
        btn.move(x, y)
        return btn

    pdfPathList = []
    directoryPath = []

    '''
    Receiving input from the User.
    -> Input is set as Folder right now.
    -> Can be swapped to single pdf by uncommenting the line below.
    '''
    def on_select_pdf_directory(self):
        file = str(QFileDialog.getExistingDirectory(self, "Select Directory", directory="."))
        self.directoryPath.append(file)
        folderContent = glob.glob(file + '/*.pdf')
        for pdfPath in folderContent:
            self.pdfPathList.append(pdfPath)

    '''
    If the input is a File
    '''
    def on_select_pdf_file(self):
        dialog = QFileDialog()
        path = QFileDialog.getOpenFileName(dialog, "wählen sie x aus", "/", "pdf(*.pdf)")
        self.pdfPathList.append(path)
    '''
    Calls the function to split the pdfs.
    '''
    def on_split_pdf(self):
        pageNumber = 1
        for pdf in self.pdfPathList:
            pdfSplitter(pdf, pageNumber)
            pageNumber += 1


    '''
    Converts the pdf's to jpeg's.
    '''
    def pdf2jpeg(self):
        pdf = wi(filename="output0.pdf", resolution=300)
        pdfImage = pdf.convert("jpeg")
        i = 1
        listImages = []
        for img in pdfImage.sequence:
            page = wi(image=img)
            page.save(filename=str(i) + ".jpeg")
            listImages.append(str(i) + ".jpeg")
            i += 1
        self.setLayout(self.populateGrid(listImages))

    '''
    Displays each pdf as an Image
    '''
    def populateGrid(self, images):
        grid = QGridLayout()

        for img in images:
            image = QPixmap(img)
            label = QLabel()
            label.setPixmap(image.scaledToWidth(80, 80))
            grid.addWidget(label)

        #self.setLayout(grid)
        return grid

    # Todo function to select which pdfs to be modified
    # Todo function to merge pdfs
    # Todo function to rotate pdfs

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PdfConverter()
    sys.exit(app.exec_())


#run the application until the user closes it
