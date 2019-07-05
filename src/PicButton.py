from src.main import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtCore import *

# Source -> https://stackoverflow.com/questions/2711033/how-code-a-image-button-in-pyqt


class PicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pixmap = self.pixmap
        if self.isDown():
            pixmap = self.pixmap_pressed
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pixmap)

    def sizeHint(self):
        return self.pixmap.size()
