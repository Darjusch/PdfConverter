import copy
import logging
import os
import uuid
from PyPDF2 import PdfFileWriter, PdfFileReader


def pdf_splitter(path_list ,checked_buttons , list_of_buttons):
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')

    for path in path_list:
        input = PdfFileReader(open(path, 'rb'))
        name_with_path = os.path.join("Output", 'output' + str(uuid.uuid1()) + ".pdf")
        output_pdf = open(name_with_path, 'wb')
        output = PdfFileWriter()

        for page_number, pdf_content in enumerate([input.getPage(page) for page in range(0, input.getNumPages())]):
            logging.info('Pagenumber: ' + str(page_number) + ' is being processed.')
            if list_of_buttons[page_number] in checked_buttons:
                logging.info('Pagenumber:' + str(page_number) + ' is being split.')
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
