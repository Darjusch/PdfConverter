from PySide2.QtCore import QSize
from PySide2.QtGui import QPixmap, QIcon, QTransform
from PySide2.QtWidgets import QPushButton
from wand.image import Image as WI
from PySide2 import QtGui


class PageObject:
    def __init__(self, page):
        self.pdf_page = page
        self.x1 = 0
        self.x2 = 1
        self.y1 = 0
        self.y2 = 1
        self.rotation = 0
        self.img = self.pageToImage(page)
        self.push_button = self.createPushButton()

    def pageToImage(self, page, fmt='png'):
        with WI(page) as page_image:
            qimage = QtGui.QImage()
            data = page_image.make_blob(format=fmt)
            qimage.loadFromData(data)
            return qimage

    def createPushButton(self):
        push_button = QPushButton()
        pixmap = QPixmap(self.img)
        icon = QIcon(pixmap)
        push_button.setIcon(icon)
        push_button.setIconSize(QSize(100, 100))
        push_button.setCheckable(True)
        return push_button

    def updateImage(self):
        self.resizeImage(self.x1, self.y1, self.x2, self.y2)

    def resizeImage(self, x1, y1, x2, y2):
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        img = self.img
        w, h = img.width(), img.height()
        self.img = img.copy(w * x1, h * y1, w * (x2 - x1), h * y2)
        self.push_button = self.createPushButton()

    def splitLeft(self):
        w = (self.x2 - self.x1) / 2
        self.resizeImage(self.x1, self.y1, self.x1 + w, self.y2)

    def splitRight(self):
        w = (self.x2 - self.x1) / 2
        self.resizeImage(self.x1 + w, self.y1, self.x2, self.y2)

    def rotate(self, rotation):
        my_transform = QTransform()
        my_transform.rotate(rotation)
        self.img = self.img.transformed(my_transform)
        self.rotation += rotation
        self.push_button = self.createPushButton()

    def convert_coordinates(self, x1, y1, width, height):
        self.x1 = (self.img.width() / x1) / 100
        self.y1 = (self.img.height() / y1) / 100
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height

