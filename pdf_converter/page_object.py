from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QIcon, QTransform
from PySide2.QtWidgets import QPushButton
from wand.image import Image as WI
from PySide2 import QtGui


class PageObject:
    def __init__(self, wi_page, original_page):
        self.page = original_page
        self.edited_lower_left_x = 0
        self.edited_lower_left_y = 0
        self.edited_upper_right_x = 1
        self.edited_upper_right_y = 1
        self.rotation = 0
        self.img = self.page_to_qimage(wi_page)
        self.push_button = self.create_push_button()

    def page_to_qimage(self, page, fmt='png'):
        with WI(page) as page_image:
            qimage = QtGui.QImage()
            data = page_image.make_blob(format=fmt)
            qimage.loadFromData(data)
            return qimage

    def create_push_button(self):
        push_button = QPushButton()
        pixmap = QPixmap(self.img)
        icon = QIcon(pixmap)
        push_button.setIcon(icon)
        push_button.setIconSize(QSize(100, 100))
        push_button.setCheckable(True)
        return push_button

    def update_image(self):
        self.resize_image(self.edited_lower_left_x, self.edited_lower_left_y, self.edited_upper_right_x, self.edited_upper_right_y)

    def resize_image(self, x1, y1, x2, y2):
        self.edited_lower_left_x, self.edited_lower_left_y, self.edited_upper_right_x, self.edited_upper_right_y = x1, y1, x2, y2
        img = self.img
        w, h = img.width(), img.height()
        self.img = img.copy(w * x1, h * y1, w * (x2 - x1), h * (y2 - y1))
        self.push_button = self.create_push_button()

    def split_left(self):
        if self.edited_lower_left_x == 0 and self.edited_upper_right_x == 1:
            w = (self.edited_upper_right_x - self.edited_lower_left_x) / 2
            self.resize_image(self.edited_lower_left_x, self.edited_lower_left_y, self.edited_lower_left_x + w, self.edited_upper_right_y)
        else:
            self.resize_image(0, 0, 0.5, 1)

    def split_right(self):
        if self.edited_lower_left_x == 0 and self.edited_upper_right_x == 1:
            w = (self.edited_upper_right_x - self.edited_lower_left_x) / 2
            self.resize_image(self.edited_lower_left_x + w, self.edited_lower_left_y, self.edited_upper_right_x, self.edited_upper_right_y)
        else:
            self.resize_image(0.5, 0, 1, 1)

    def rotate(self, rotation):
        my_transform = QTransform()
        my_transform.rotate(rotation)
        self.img = self.img.transformed(my_transform)
        self.rotation = self.rotation + rotation
        self.push_button = self.create_push_button()

    # 1 is 100 %, 0.5 = 50 % ..
    def convert_coordinates_into_percentage(self, x1, y1, width, height):
        try:
            self.edited_lower_left_x = 1 / (self.img.width() / x1)
        except ZeroDivisionError:
            self.edited_lower_left_x = 1 / self.img.width()
            print(ZeroDivisionError)
        try:
            self.edited_lower_left_y = 1 / (self.img.height() / y1)
        except ZeroDivisionError:
            self.edited_lower_left_y = 1 / self.img.height()
        try:
            self.edited_upper_right_x = self.edited_lower_left_x + (1 / (self.img.width() / width))
        except ZeroDivisionError:
            self.edited_upper_right_x = self.edited_lower_left_x + (1 / self.img.width())
        try:
            self.edited_upper_right_y = self.edited_lower_left_y + (1 / (self.img.height() / height))
        except ZeroDivisionError:
            self.edited_upper_right_y = self.edited_lower_left_y + (1 / self.img.height())
