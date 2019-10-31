from PySide2.QtCore import QSize, QRect
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QMainWindow, QLabel, QRubberBand


class PdfPageWindow(QMainWindow):
    def __init__(self, page_obj, parent=None):
        super(PdfPageWindow, self).__init__()
        self.resize(1920, 1080)
        self.parent = parent
        self.page_obj = page_obj
        self.index = self.parent.page_objects.index(page_obj)
        self.pixmap = QPixmap(page_obj.img)
        self.label = QLabel(self)
        self.label.setPixmap(self.pixmap)
        self.x1 = int(self.width() / 2) - 400
        self.y1 = int(self.height() / 2) - 300
        self.x2 = self.pixmap.width()
        self.y2 = self.pixmap.height()
        self.label.setGeometry(QRect(self.x1, self.y1, self.x2, self.y2))

    def mousePressEvent(self, mouse_click_event):
        self.origin_mouse_pos = mouse_click_event.pos()
        self.current_rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.current_rubber_band.setGeometry(QRect(self.origin_mouse_pos, QSize()))
        self.current_rubber_band.show()

    def mouseMoveEvent(self, mouse_click_event):
        self.current_rubber_band.setGeometry(QRect(self.origin_mouse_pos, mouse_click_event.pos()).normalized())

    def mouseReleaseEvent(self, mouse_click_event):
        self.current_rubber_band.hide()
        rubber_band_rect = self.current_rubber_band.geometry()
        current_q_rect = QRect(rubber_band_rect.x()-self.x1, rubber_band_rect.y()-self.y1,
                               rubber_band_rect.width(), rubber_band_rect.height())
        self.current_rubber_band.deleteLater()
        self.pixmap = self.pixmap.copy(current_q_rect)
        crop_q_pixmap = self.pixmap
        crop_q_pixmap.save('output.png')
        self.page_obj.convert_coordinates(current_q_rect.x(), current_q_rect.y(),
                                          current_q_rect.width(), current_q_rect.height())
        self.page_obj.img.save('page_obj.png')
        self.page_obj.update_image()
        self.page_obj.img.save('after_update.png')
        self.parent.page_objects.remove(self.parent.page_objects[self.index])
        #self.page_obj(self.page_obj.page)
        self.page_obj.create_push_button()
        self.parent.page_objects.insert(self.index, self.page_obj)
        self.parent.delete_push_button_from_grid()
        self.parent.position_push_button_in_grid()
