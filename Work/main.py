from sys import argv, exit
from typing import Optional

from PyQt6.QtCore import pyqtSignal, pyqtBoundSignal, Qt
from PyQt6.QtGui import QPixmap, QImage, QKeyEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

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
        self.setFixedSize(700, 750)
        self.button = QPushButton('Светлая/Тёмная', self)
        self.button.move(580, 70)
        self.add_post = QPushButton('Добавить/убрать индекс', self)
        self.add_post.adjustSize()
        self.add_post.move(20, 580)
        self.need_postal: bool = False
        self.text: list[str, str] = ['', '']
        bound: pyqtSignal | pyqtBoundSignal = self.add_post.clicked
        bound.connect(lambda: setattr(self, 'need_postal', not self.need_postal) or (self.address_error.setText(
            ', '.join(self.text) if self.need_postal else self.text[0])))

        bound: pyqtSignal | pyqtBoundSignal = self.reset_btn.clicked
        bound.connect(self.reset)

        bound: pyqtSignal | pyqtBoundSignal = self.search_btn.clicked
        bound.connect(self.search)

        bound: pyqtSignal | pyqtBoundSignal = self.button.clicked
        bound.connect(self.set_theme)

        self.current_theme = 'light'
        self.marked_point: list[tuple[float, float], ...] = list()
        self.zoom = 17
        self.current_pos = None
        self.set_default_position()
        self.set_image()

    def reset(self):
        self.marked_point = list()
        self.address_error.clear()
        self.search_area.clear()
        self.set_image()

    def search(self):
        request = self.search_area.text()
        if not request:
            return
        params = {
            'apikey': GEOCODE_API_KEY,
            'geocode': request,
            'format': 'json'
        }
        obj = get_object(get_geocode_data(**params))
        coords = get_coord_from_object(obj)
        locality = get_address_and_postal_code_from_geocode_obj(obj)
        address, postal_code = self.text = locality
        self.address_error.setText(address + f', {postal_code}' if self.need_postal else address)
        self.current_pos = list(coords)
        self.marked_point = coords
        self.search_area.clearFocus()
        self.set_image()

    def set_default_position(self):
        params = {
            'apikey': GEOCODE_API_KEY,
            'format': 'json',
            'geocode': 'Краснодар, Бульварное кольцо,  9'
        }
        self.current_pos = list(get_coord_from_object(get_object(get_geocode_data(**params))))

    def set_theme(self):
        self.current_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.set_image()

    def set_image(self):
        params = {
            'apikey': STATIC_MAPS_API_KEY,
            'll': ','.join(map(str, self.current_pos)),
            'z': self.zoom,
            'size': '650,450',
            'theme': self.current_theme
        }
        if self.marked_point:
            params['pt'] = ','.join(map(str, self.marked_point)) + ',pm2gnl'
        data = get_image_from_coord(**params)
        self.label.setPixmap(QPixmap.fromImage(QImage.fromData(data)))

    def keyReleaseEvent(self, event: Optional[QKeyEvent]) -> None:
        if event.key() == Qt.Key.Key_Up:
            self.current_pos[1] *= (1.000008 + 0.000005 * (21 - self.zoom))
        elif event.key() == Qt.Key.Key_Down:
            self.current_pos[1] /= (1.000008 + 0.000005 * (21 - self.zoom))
        elif event.key() == Qt.Key.Key_Left:
            self.current_pos[0] /= (1.000008 + 0.000005 * (21 - self.zoom))
        elif event.key() == Qt.Key.Key_Right:
            self.current_pos[0] *= (1.000008 + 0.000005 * (21 - self.zoom))
        self.set_image()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_PageUp:
            self.zoom = min(21, self.zoom + 1)
        elif event.key() == Qt.Key.Key_PageDown:
            self.zoom = max(0, self.zoom - 1)
        elif event.key() == Qt.Key.Key_Return:
            self.search()
        else:
            return
        self.set_image()


if __name__ == '__main__':
    application = QApplication(argv)
    window = SearchMapApp()
    window.show()
    exit(application.exec())
