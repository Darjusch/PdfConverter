from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QAbstractButton


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.clicked.connect(self.resize)
        self.rotate = 0

    def paintEvent(self, event):
        pixmap = self.pixmap
        painter = QPainter(self)
        if self.isChecked(): # Todo only if rotate button is clicked rotate. we have to fix this -> src.main.PdfConverter.rotate_button(self).isClicked()
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
