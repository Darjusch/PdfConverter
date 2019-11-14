import copy

from PyPDF2 import PdfFileWriter


class Logic:

    def create_pdf_action_handler(self, page_objects):
        original_pdf_writer = PdfFileWriter()
        for page_object in page_objects:
            page_object.page = copy.copy(page_object.page)
            page_object.page, x1, y1, x2, y2 = self.adjust_coordinates(page_object)
            self.adjust_pdf(page_object.page, x1, y1, x2, y2)
            page_object.page.rotateClockwise(page_object.rotation * 0.5)
            original_pdf_writer.addPage(page_object.page)
        with open('original.pdf', 'wb') as original_pdf:
            original_pdf_writer.write(original_pdf)


    def adjust_coordinates(self, page_object):
        x1, y1, x2, y2 = page_object.x1, page_object.y1, page_object.x2, page_object.y2
        page = page_object.page.mediaBox
        original_x1, original_y1, original_x2, original_y2 = page.getLowerLeft_x(), \
                                                             page.getLowerLeft_y(), \
                                                             page.getUpperRight_x(), \
                                                             page.getUpperRight_y()
        lower_left_x, lower_left_y, upper_right_x, upper_right_y = \
            int(original_x2) * x1,\
            int(original_y1) * y1,\
            int(original_x2) * x2,\
            int(original_y2) * y2
        print(f'x1 to x2:  {lower_left_x} to {upper_right_x}')
        return page_object.page, int(lower_left_x), int(lower_left_y), int(upper_right_x), int(upper_right_y)


    def adjust_pdf(self, page, x1, y1, x2, y2):
        page.mediaBox.lowerLeft = (x1, y1)
        page.mediaBox.upperRight = (x2, y2)
