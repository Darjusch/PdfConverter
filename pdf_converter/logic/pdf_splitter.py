import copy
import logging
import logging.config
import os
import uuid
from PyPDF2 import PdfFileWriter, PdfFileReader


def pdf_splitter(path ,checked_buttons , list_of_buttons):
    #logging.config.fileConfig(fname='logging.config', disable_existing_loggers=False)
    #logger = logging.getLogger(__name__)

    input = PdfFileReader(open(path, 'rb'))
    name_with_path = os.path.join("../output/" + str(uuid.uuid1()) + ".pdf")
    output_pdf = open(name_with_path, 'wb')
    output = PdfFileWriter()

    for page_number, pdf_content in enumerate([input.getPage(page) for page in range(0, input.getNumPages())]):
        logging.info('Pagenumber: %s is being processed.', str(page_number))
        if list_of_buttons[page_number] in checked_buttons:
            logging.info('Pagenumber: %s is being split.', str(page_number))
            left, right = split(pdf_content)
            # In python even numbers are True and odd numbers are False
            if page_number or page_number is 0:
                output.addPage(left)
            output.addPage(right)
        else:
            output.addPage(pdf_content)

    output.write(output_pdf)
    output_pdf.close()


def split(pdf_content):
    pdf_content_left = copy.copy(pdf_content)
    pdf_content_right = copy.copy(pdf_content)
    (w, h) = pdf_content.mediaBox.upperRight
    pdf_content_left.mediaBox.upperRight = (w / 2, h)
    pdf_content_right.mediaBox.upperLeft = (w / 2, h)
    return pdf_content_left, pdf_content_right
