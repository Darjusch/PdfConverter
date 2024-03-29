from PyPDF2 import PdfFileWriter, PdfFileReader
from pdf_converter.main import MainWindow
import logging
import logging.config


def pdf_cropper(self):
    logging.config.fileConfig(fname='logging.config', disable_existing_loggers=False)
    logger = logging.getLogger(__name__)

    for button in MainWindow.checked_buttons(self):
        if button.isChecked():
            file = PdfFileReader(open(self.pdf_path_list[0], "rb"))
            page = file.getPage(0)
            page.mediaBox.lowerRight = (
            self.upper_right_new_x_coordinate.text(), self.upper_right_new_y_coordinate.text())
            page.mediaBox.lowerLeft = (self.lower_left_new_x_coordinate.text(), self.lower_left_new_y_coordinate.text())
            page.mediaBox.upperRight = (
            self.lower_right_new_x_coordinate.text(), self.lower_right_new_y_coordinate.text())
            page.mediaBox.upperLeft = (self.upper_left_new_x_coordinate.text(), self.upper_left_new_y_coordinate.text())
            output = PdfFileWriter()
            output.addPage(page)
            output.write(open("cropped.pdf", "wb"))
            logging.info("Page: %s is being processed!", page)
