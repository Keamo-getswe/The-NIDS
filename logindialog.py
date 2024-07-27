from PySide6 import QtWidgets
from PySide6.QtWidgets import (QDialog, QLineEdit, QPushButton, 
                               QVBoxLayout, QHBoxLayout, QLabel,
                               QApplication)

class LoginWidget(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self._WIDTH = 300
        self._HEIGHT = 250
        self._init_components()
        self._setup_gui()
        self._set_window_position()

        self._submit_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)

    def _init_components(self):
        self._username_edit = QLineEdit()
        self._password_edit = QLineEdit()
        self._submit_button = QPushButton("Submit")
        self._cancel_button = QPushButton("Cancel")

        self._main_layout = QVBoxLayout()
        self._username_layout = QVBoxLayout()
        self._password_layout = QVBoxLayout()
        self._button_layout = QHBoxLayout()

    def _setup_gui(self):
        self.username_label = QLabel("Enter Username:")
        self._username_layout.addWidget(self.username_label)
        self._username_layout.addWidget(self._username_edit)

        password_label = QLabel("Enter Password:")
        self._password_layout.addWidget(password_label)
        self._password_layout.addWidget(self._password_edit)

        self._button_layout.addWidget(self._submit_button)
        self._button_layout.addWidget(self._cancel_button)

        self._main_layout.addLayout(self._username_layout)
        self._main_layout.addLayout(self._password_layout)
        self._main_layout.addLayout(self._button_layout)
        self.setLayout(self._main_layout)
    
    def _set_window_position(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        x = screen_geometry.width()/2 - self._WIDTH/4
        y = screen_geometry.height()/2 - self._HEIGHT/4
        self.move(x, y)

    def get_username(self):
        return self._username_edit.text()
    
    def get_password(self):
        return self._password_edit.text()




