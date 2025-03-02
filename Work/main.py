from sys import argv, exit

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow

from API_KEYS import *
from Work.UI.Window import Ui_MainWindow
from utils import *

STATIC_MAPS_API_KEY = STATIC_MAPS_API_KEY
GEOCODE_API_KEY = GEOCODE_API_KEY
SEARCH_MAPS_API_KEY = SEARCH_MAPS_API_KEY


class SearchMapApp(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(650, 450)
        self.zoom = 17
        self.set_image()

    def set_image(self):
        params = {
            'apikey': GEOCODE_API_KEY,
            'format': 'json',
            'geocode': 'Краснодар, Бульварное кольцо,  9'
        }
        coords = get_coord_from_object(get_object(get_geocode_data(**params)))
        coords = ','.join(map(str, coords))
        params = {
            'apikey': STATIC_MAPS_API_KEY,
            'll': coords,
            'z': self.zoom,
            'size': '650,450'
        }
        data = get_image_from_coord(**params)
        self.label.setPixmap(QPixmap.fromImage(QImage.fromData(data)))

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_PageUp:
            self.zoom = min(21, self.zoom + 1)
        elif event.key() == Qt.Key.Key_PageDown:
            self.zoom = max(0, self.zoom - 1)
        else:
            return
        self.set_image()


if __name__ == '__main__':
    application = QApplication(argv)
    window = SearchMapApp()
    window.show()
    exit(application.exec())
