from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QLabel, QHBoxLayout, QGridLayout,
                                QPushButton, QWidget, QTextEdit,
                                QGroupBox)
from logreader import LogReader

class LogDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self._init_components()
        self._set_gui()

        self._refresh_button.clicked.connect(self.load_log)

    @QtCore.Slot()
    def load_log(self):
        data = self.reader.read()
        self._log_view.setText(data)

    def _init_components(self):
        self.reader = LogReader()
        self._section_label = QLabel("Log Dashboard")
        self._refresh_button = QPushButton("Refresh")
        self._button_layout = QHBoxLayout()
        self._main_layout = QGridLayout()
        self._button_group = QGroupBox()
        self._log_view = QTextEdit()

        self._button_layout.setStretch(0, 1)
        self._button_layout.setStretch(1, 1)

        self._log_view.setReadOnly(True)
        font = QFont()
        font.setPointSize(14)
        self._log_view.setFont(font)
        self.load_log()

    def _set_gui(self):
        button_width = 75
        button_height = 25
        button_group_width = 200
        button_group_height = 80

        self._refresh_button.setFixedSize(button_width, button_height)

        self._button_layout.addWidget(self._refresh_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self._button_group.setLayout(self._button_layout)
        self._button_group.setFixedSize(button_group_width, button_group_height)
        
        font = self._section_label.font()
        font.setPointSize(28)
        self._section_label.setFont(font)
        
        self._main_layout.addWidget(self._section_label, 0, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self._main_layout.addWidget(self._button_group, 1, 0)
        self._main_layout.addWidget(self._log_view, 2, 0)

        self.setLayout(self._main_layout)
        