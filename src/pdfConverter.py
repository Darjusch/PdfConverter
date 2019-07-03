import copy
import logging
from multiprocessing import Pool

from PyPDF2 import PdfFileWriter, PdfFileReader


def pdfSplitter(path, pageNumber):
    logging.getLogger().setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s %(message)s')

    input = PdfFileReader(open(path, 'rb'))
    outputPdf = open('output' + str(pageNumber) + ".pdf", 'wb')
    output = PdfFileWriter()
    # for nn,p in enumerate([input.getPage(i) for i in range(0,10)]):
    for pageNumber, pdfContent in enumerate([input.getPage(i) for i in range(0, input.getNumPages())]):
        logging.info('Pagenumber: ' + str(pageNumber) + ' is being processed.')
        left, right = split(pdfContent)

        if pageNumber or pageNumber is 0:
            output.addPage(left)
        output.addPage(right)

    output.write(outputPdf)

def split(pdfContent):
    pdfContentLeft = copy.copy(pdfContent)
    pdfContentRight = copy.copy(pdfContent)
    (w, h) = pdfContent.mediaBox.upperRight
    pdfContentLeft.mediaBox.upperRight = (w / 2, h)
    pdfContentRight.mediaBox.upperLeft = (w / 2, h)
    return pdfContentLeft, pdfContentRight

#def fastPdfSplitter(path, pageNumber, self):
#    with Pool(processes=4) as pool:
#        pass