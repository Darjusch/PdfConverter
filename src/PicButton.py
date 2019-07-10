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
        self.clicked.connect(self.resize)
        #self.pressed.connect(self.update)
        #self.released.connect(self.update)

    '''
    If the button is clicked the image changes and the button is marked as checked.
    -> If clicked again the button is unmarked again.
    '''
    def paintEvent(self, event):
        pixmap = self.pixmap
        if self.isDown():
            pixmap = self.pixmap_pressed
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pixmap)

    def sizeHint(self):
        return self.pixmap.size()

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def resize(self, *__args):
        if self.isChecked():
            self.setFixedWidth(100)
            self.setFixedHeight(100)
        else:
            self.setFixedWidth(200)
            self.setFixedHeight(200)