from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QIcon, QTransform, QImage
from PySide2.QtWidgets import QPushButton
from wand.image import Image as WandImageFrom


class PageObject:
    def __init__(self, wi_image, original_page):
        self.page = original_page
        self.wi_image = wi_image
        self.current_lower_left_x = 0
        self.current_lower_left_y = 0
        self.current_upper_right_x = 1
        self.current_upper_right_y = 1
        self.updated_lower_left_x = self.current_lower_left_x
        self.updated_lower_left_y = self.current_lower_left_y
        self.updated_upper_right_x = self.current_upper_right_x
        self.updated_upper_right_y = self.current_upper_right_y
        self.rotation = 0
        self.img = None
        self.push_button = None
        self.page_to_qimage()
        self.create_push_button()


    def page_to_qimage(self, fmt='png'):
        with WandImageFrom(self.wi_image) as page_image:
            qimage = QImage()
            data = page_image.make_blob(format=fmt)
            qimage.loadFromData(data)
            self.img = qimage

    def create_push_button(self):
        push_button = QPushButton()
        pixmap = QPixmap(self.img)
        if pixmap.width() > 140 and pixmap.height() > 150:
            pixmap = pixmap.scaled(130, 155)
        else:
            if pixmap.width() < 140:
                pixmap = pixmap.scaled(65, 155)
            elif pixmap.height() < 220:
                pixmap = pixmap.scaled(130, 70)

        icon = QIcon(pixmap)
        w = pixmap.width()
        h = pixmap.height()
        push_button.setIcon(icon)
        push_button.setIconSize(QSize(w, h))
        push_button.setFixedSize(QSize(w+26, h+26))
        push_button.setCheckable(True)
        self.push_button = push_button

    def split_left(self):
        if self.current_lower_left_x == 0 and self.current_upper_right_x == 1:
            w = (self.current_upper_right_x - self.current_lower_left_x) / 2
            self.updated_upper_right_x = self.current_lower_left_x + w
        else:
            self.updated_lower_left_x, self.updated_lower_left_y, self.updated_upper_right_x, self.updated_upper_right_y = 0, 0, 0.5, 1
        self.updated_coordinates()

    def split_right(self):
        if self.current_lower_left_x == 0 and self.current_upper_right_x == 1:
            w = (self.current_upper_right_x - self.current_lower_left_x) / 2
            self.updated_lower_left_x = self.current_lower_left_x + w
        else:
            self.updated_lower_left_x, self.updated_lower_left_y, self.updated_upper_right_x, self.updated_upper_right_y = 0.5, 0, 1, 1
        self.updated_coordinates()

    def resize_image(self):
        w, h = self.img.width(), self.img.height()
        self.img = self.img.copy(w * self.current_lower_left_x,
                                 h * self.current_lower_left_y,
                                 w * (self.current_upper_right_x - self.current_lower_left_x),
                                 h * (self.current_upper_right_y - self.current_lower_left_y))
        self.create_push_button()

    def updated_coordinates(self):
        self.current_lower_left_x, self.current_lower_left_y, self.current_upper_right_x, self.current_upper_right_y = self.updated_lower_left_x, \
                                                                                                                       self.updated_lower_left_y, \
                                                                                                                       self.updated_upper_right_x, \
                                                                                                                       self.updated_upper_right_y
        self.resize_image()

    def rotate_image_update_rotation_and_push_button(self, rotation):
        my_transform = QTransform()
        my_transform.rotate(rotation)
        self.img = self.img.transformed(my_transform)
        self.rotation = self.rotation + rotation
        self.create_push_button()

    # 1 is 100 %, 0.5 = 50 % ..
    def convert_coordinates_into_decimal_percentage(self, x1, y1, width, height):
        try:
            self.current_lower_left_x = 1 / (self.img.width() / x1)
        except ZeroDivisionError:
            self.current_lower_left_x = 1 / self.img.width()
        try:
            self.current_lower_left_y = 1 / (self.img.height() / y1)
        except ZeroDivisionError:
            self.current_lower_left_y = 1 / self.img.height()
        try:
            self.current_upper_right_x = self.current_lower_left_x + (1 / (self.img.width() / width))
        except ZeroDivisionError:
            self.current_upper_right_x = self.current_lower_left_x + (1 / self.img.width())
        try:
            self.current_upper_right_y = self.current_lower_left_y + (1 / (self.img.height() / height))
        except ZeroDivisionError:
            self.current_upper_right_y = self.current_lower_left_y + (1 / self.img.height())
