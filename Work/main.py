from sys import argv, exit

from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow

from Work.UI.Window import Ui_MainWindow
from utils import *

STATIC_MAPS_API_KEY = "YOUR_API_KEY"
GEOCODE_API_KEY = "YOUR_API_KEY"
SEARCH_MAPS_API_KEY = "YOUR_API_KEY"


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


if __name__ == '__main__':
    application = QApplication(argv)
    window = SearchMapApp()
    window.show()
    exit(application.exec())
