from src.main import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAbstractButton


# Source -> https://stackoverflow.com/questions/2711033/how-code-a-image-button-in-pyqt


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()
