from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QIcon, QTransform
from PySide2.QtWidgets import QPushButton
from wand.image import Image as WI
from PySide2 import QtGui


class PageObject:
    def __init__(self, wi_page, original_page):
        self.page = original_page
        self.x1 = 0
        self.x2 = 1
        self.y1 = 0
        self.y2 = 1
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
        self.resize_image(self.x1, self.y1, self.x2, self.y2)

    def resize_image(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        img = self.img
        w, h = img.width(), img.height()
        self.img = img.copy(w * x1, h * y1, w * (x2 - x1), h * (y2 - y1))
        self.push_button = self.create_push_button()

    def split_left(self):
        if self.x1 == 0 and self.x2 == 1:
            w = (self.x2 - self.x1) / 2
            self.resize_image(self.x1, self.y1, self.x1 + w, self.y2)
        else:
            self.resize_image(0, 0, 0.5, 1)

    def split_right(self):
        if self.x1 == 0 and self.x2 == 1:
            w = (self.x2 - self.x1) / 2
            self.resize_image(self.x1 + w, self.y1, self.x2, self.y2)
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
            self.x1 = 1 / (self.img.width() / x1)
        except ZeroDivisionError:
            self.x1 = 1 / self.img.width()
            print(ZeroDivisionError)
        try:
            self.y1 = 1 / (self.img.height() / y1)
        except ZeroDivisionError:
            self.y1 = 1 / self.img.height()
        try:
            self.x2 = self.x1 + (1 / (self.img.width() / width))
        except ZeroDivisionError:
            self.x2 = self.x1 + (1 / self.img.width())
        try:
            self.y2 = self.y1 + (1 / (self.img.height() / height))
        except ZeroDivisionError:
            self.y2 = self.y1 + (1 / self.img.height())
