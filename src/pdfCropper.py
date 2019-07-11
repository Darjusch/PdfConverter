from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger


def pdf_cropper():
    file = PdfFileReader(open("KW22_Version_A_mOeffnungszeiten_2505-3105 Kopie 2.pdf", "rb"))
    page = file.getPage(0)
    print(page.cropBox.getLowerLeft())
    print(page.cropBox.getLowerRight())
    print(page.cropBox.getUpperLeft())
    print(page.cropBox.getUpperRight())
    lower_right_new_x_coordinate = 611
    lower_right_new_y_coordinate = 500
    lower_left_new_x_coordinate = 0
    lower_left_new_y_coordinate = 500
    upper_right_new_x_coordinate = 611
    upper_right_new_y_coordinate = 700
    upper_left_new_x_coordinate = 0
    upper_left_new_y_coordinate = 700
    page.mediaBox.lowerRight = (lower_right_new_x_coordinate, lower_right_new_y_coordinate)
    page.mediaBox.lowerLeft = (lower_left_new_x_coordinate, lower_left_new_y_coordinate)
    page.mediaBox.upperRight = (upper_right_new_x_coordinate, upper_right_new_y_coordinate)
    page.mediaBox.upperLeft = (upper_left_new_x_coordinate, upper_left_new_y_coordinate)
