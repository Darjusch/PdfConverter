import copy
from PyPDF2 import PdfFileWriter


class Logic:
    def __init__(self):
        self.page = None
        self.page_object = None
        self.output_lower_left_x = None
        self.output_lower_left_y = None
        self.output_upper_right_x = None
        self.output_upper_right_y = None
        self.output_pdf_writer = PdfFileWriter()

    def create_pdf_action_handler(self, page_objects):
        for page_object in page_objects:
            self.page_object = page_object
            self.page = page_object.page
            self.create_copy_of_page()
        self.write_adjusted_output_pdf()

    def create_copy_of_page(self):
        self.page = copy.copy(self.page)
        self.adjust_coordinates_of_output_pdf_to_edited_pdf()

    def adjust_coordinates_of_output_pdf_to_edited_pdf(self):
        self.output_lower_left_x, self.output_lower_left_y, self.output_upper_right_x, self.output_upper_right_y = \
                                                int(int(self.page.mediaBox.getUpperRight_x()) * self.page_object.current_lower_left_x),\
                                                int(int(self.page.mediaBox.getLowerLeft_y()) * self.page_object.current_lower_left_y),\
                                                int(int(self.page.mediaBox.getUpperRight_x()) * self.page_object.current_upper_right_x),\
                                                int(int(self.page.mediaBox.getUpperRight_y()) * self.page_object.current_upper_right_y)
        self.adjust_output_pdf_according_to_new_coordinates()

    def adjust_output_pdf_according_to_new_coordinates(self):
        self.page.mediaBox.lowerLeft = (self.output_lower_left_x, self.output_lower_left_y)
        self.page.mediaBox.upperRight = (self.output_upper_right_x, self.output_upper_right_y)
        self.rotate_output_pdf_according_to_edited_pdf_rotation()

    def rotate_output_pdf_according_to_edited_pdf_rotation(self):
        self.page.rotateClockwise(self.page_object.rotation*0.5)
        self.add_adjusted_output_page()

    def add_adjusted_output_page(self):
        self.output_pdf_writer.addPage(self.page)

    def write_adjusted_output_pdf(self):
        with open('output_pdf.pdf', 'wb') as output_pdf:
            self.output_pdf_writer.write(output_pdf)

