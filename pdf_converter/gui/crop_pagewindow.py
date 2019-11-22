from PySide2.QtCore import QSize, QRect
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMainWindow, QLabel, QRubberBand, QWidget, QGridLayout, QScrollArea, QPushButton


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
        self.selected_area_in_page_window_to_area_in_image()
        self.selected_area_in_pagewindow.deleteLater()
        self.page_obj.update_image()
        self.parent.page_objects.remove(self.parent.page_objects[self.index])
        self.parent.page_objects.insert(self.index, self.page_obj)
        self.parent.delete_push_button_from_grid()
        self.parent.position_push_button_in_grid()

    def selected_area_in_page_window_to_area_in_image(self):
        selected_area_in_page_window_rectangle = self.selected_area_in_pagewindow.geometry()
        selected_area_in_image_rectangle = \
            QRect(selected_area_in_page_window_rectangle.x()-self.x1,
                  selected_area_in_page_window_rectangle.y()-self.y1,
                  selected_area_in_page_window_rectangle.width(),
                  selected_area_in_page_window_rectangle.height()
                  )
        self.convert_coordinates_to_percentage(selected_area_in_image_rectangle)

    def convert_coordinates_to_percentage(self, selected_area_in_image_rectangle):
        self.page_obj.convert_coordinates_into_percentage(
            selected_area_in_image_rectangle.x(),
            selected_area_in_image_rectangle.y(),
            selected_area_in_image_rectangle.width(),
            selected_area_in_image_rectangle.height()
        )
