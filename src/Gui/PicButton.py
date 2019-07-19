from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QAbstractButton
from src.main import PdfConverter

class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.clicked.connect(self.resize)
        self.rotate = 0

    def paintEvent(self, event):
        pixmap = self.pixmap
        painter = QPainter(self)
        if self.isChecked() and PdfConverter.rotate_button(self).isClicked():
            painter.translate(self.width(), 0)
            self.rotate += 90
            self.rotate %= 360
            painter.rotate(90)
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
