class PageObject:
    def __init__(self, page):
        self.pdf_page = page
        self.x1 = 0
        self.x2 = 1
        self.y1 = 0
        self.y2 = 1
        self.rotation = 0

    def pageToImage(self):
        pass