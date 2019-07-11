import copy
import logging
import os
from multiprocessing import Pool
from PyPDF2 import PdfFileWriter, PdfFileReader


def pdf_splitter(checked_buttons, path):
    page_number = 0
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')
    input = PdfFileReader(open(path, 'rb'))
    save_path = "Output"
    name_with_path = os.path.join(save_path, 'output' + str(page_number) + ".pdf")
    page_number += 1
    output_pdf = open(name_with_path, 'wb')
    output = PdfFileWriter()

    # Todo split into 2 for loops for more readability

    for page_number, pdf_content in enumerate([input.getPage(i) for i in range(0, input.getNumPages())]):
        logging.info('Pagenumber: ' + str(page_number) + ' is being processed.')
        if page_number in checked_buttons:
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

#def fastPdfSplitter(path, pageNumber):
#    with Pool(processes=4) as pool:
#        pass