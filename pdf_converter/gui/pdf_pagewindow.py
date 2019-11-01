from PySide2.QtCore import QSize, QRect
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMainWindow, QLabel, QRubberBand


class PdfPageWindow(QMainWindow):
    def __init__(self, page_obj, parent=None):
        super(PdfPageWindow, self).__init__()
        self.resize(1440, 811)
        self.parent = parent
        self.page_obj = page_obj
        self.index = self.parent.page_objects.index(page_obj)
        self.pixmap = QPixmap(page_obj.img)
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.x1 = int((self.width() - self.pixmap.width()) / 2)
        self.y1 = int((self.height() - self.pixmap.height()) / 2)
        self.x2 = self.pixmap.width()
        self.y2 = self.pixmap.height()
        self.label.setGeometry(QRect(self.x1, self.y1, self.x2, self.y2))

    def mousePressEvent(self, mouse_click_event):
        self.origin_mouse_position = mouse_click_event.pos()
        self.selected_area_in_pagewindow = QRubberBand(QRubberBand.Rectangle, self)
        self.selected_area_in_pagewindow.setGeometry(
            QRect(
                self.origin_mouse_position,
                QSize()
            )
        )
        self.selected_area_in_pagewindow.show()

    def mouseMoveEvent(self, mouse_click_event):
        self.selected_area_in_pagewindow.setGeometry(
            QRect(
                self.origin_mouse_position,
                mouse_click_event.pos()
            ).normalized()
        )

    def mouseReleaseEvent(self, mouse_click_event):
        self.selected_area_in_pagewindow.hide()
        selected_area_in_pagewindow_rectangle = self.selected_area_in_pagewindow.geometry()
        # Because we are working with windows the starting point is always in the top left corner and not in the lower left.
        # selected_area_in_pagewindow_rectangle.x() and selected_area_in_pagewindow_rectangle.y() tells you
        # where the image of the pdf_page is located inside the main window
        # selected_area_in_pagewindow_rectangle.width() and selected_area_in_pagewindow_rectangle.height() tells you
        # the width and height of the selected area inside the image
        # we take the x and y position in the window minus the x and y position of the picture
        # to save the changes for the pdf later on.
        selected_area_in_image_rectangle = \
            QRect(selected_area_in_pagewindow_rectangle.x()-self.x1,
                  selected_area_in_pagewindow_rectangle.y()-self.y1,
                  selected_area_in_pagewindow_rectangle.width(),
                  selected_area_in_pagewindow_rectangle.height()
                  )
        self.selected_area_in_pagewindow.deleteLater()
        #self.pixmap = self.pixmap.copy(selected_area_in_image_rectangle)
        #cropped_pixmap = self.pixmap
        #cropped_pixmap.save('cropped_area.png')
        # Takes the current q rect and converts its coordinates into a percentage range
        # where 1 is 100 % ,0.5 == 50% and 0 is 0 %
        # Because we want to change the pdf in the end and we cant work with pixels with out destroying the pdf structure.
        self.page_obj.convert_coordinates_into_percentage(
            selected_area_in_image_rectangle.x(),
            selected_area_in_image_rectangle.y(),
            selected_area_in_image_rectangle.width(),
            selected_area_in_image_rectangle.height()
        )
        #self.page_obj.img.save('whole_img.png')
        self.page_obj.update_image()
        #self.page_obj.img.save('after_cropping.png')
        self.parent.page_objects.remove(self.parent.page_objects[self.index])
        self.parent.page_objects.insert(self.index, self.page_obj)
        self.parent.delete_push_button_from_grid()
        self.parent.position_push_button_in_grid()
