from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import (QLabel, QPushButton, QVBoxLayout)
from PySide6.QtGui import (QPixmap, QIcon, QFont)
from PySide6.QtCore import Qt
import utility

class CardWidget(QtWidgets.QPushButton):
    def __init__(self, icon_name, card_title):
        super().__init__()

        self._WIDTH = 400
        self._HEIGHT = 300

        self._icon_name = icon_name
        self._card_title = card_title

        self._init_components()
        self._set_gui()

    def _init_components(self):
        self._title_label = QLabel(self._card_title)
        self._icon_label = QLabel()
        self._layout = QVBoxLayout()
        

    def _set_gui(self):
        # Redacted
        icon_path = utility.ICON_PATH + self._icon_name
        self._icon_label.setPixmap(QPixmap(icon_path))

        font = self._title_label.font()
        font.setPointSize(32)
        self._title_label.setFont(font)

        self._layout.addWidget(self._title_label, 0, Qt.AlignmentFlag.AlignCenter)
        self._layout.addWidget(self._icon_label, 0, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)
        self.setFixedSize(self._WIDTH, self._HEIGHT)