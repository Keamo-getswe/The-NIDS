from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import (QGroupBox, QHBoxLayout, QLabel,
                               QDialog, QApplication, QGridLayout,
                               QWidget, QMenu, QMenuBar,
                                QToolBar, QStyle)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from logindialog import LoginWidget
from cardwidget import CardWidget
from anomalydashboard import AnomalyDashboard
from signaturedashboard import SignatureDashboard
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._loginDialog = LoginWidget()
        self._run_login()

        self._init_components()
        self._setup_gui()
        self._init_window_dimensions()

        self._cards[0].clicked.connect(self.show_anomaly_dashboard)
        self._cards[1].clicked.connect(self.show_signature_dashboard)

    def set_central(self, widget):
        if self._current_central_widget != None:
            self._current_central_widget.setParent(None)

        self._current_central_widget = widget
        self.setCentralWidget(self._current_central_widget)

    @QtCore.Slot()
    def show_main_dashboard(self):
        self.set_central(self._main_dash)

    @QtCore.Slot()
    def show_anomaly_dashboard(self):
        self.set_central(self._anomaly_dash)

    @QtCore.Slot()
    def show_signature_dashboard(self):
        self.set_central(self._signature_dash)

    def _init_components(self):
        self._cards = []
        icon_names = [
            "anonymous-user-icon.png",
            "database-bug-icon.png",
            "column-chart-icon.png",
            "writing-icon.png"
        ]
        card_titles = [
            "Anomalies",
            "Signatures",
            "Statistics",
            "Logs"
        ]

        for i in range(4):
            self._cards += [CardWidget(icon_names[i], card_titles[i])]

        self._board_layout = QGridLayout()
        self._main_layout = QGridLayout()
        self._main_dash = QWidget()
        self._section_label = QLabel("Main Dashboard")

        self._file_menu = self.menuBar().addMenu("File")
        self._exit_action = QAction("Exit", self)

        self._tool_menu = self.menuBar().addMenu("Tools")
        self._start_monitor_menu = QMenu("Start Monitoring...")
        self._start_anom_monitor = QAction("Anomalies", self)
        self._start_sig_monitor = QAction("Signatures", self)
        self._stop_monitor_menu = QMenu("Stop Monitoring...")
        self._stop_anom_monitor = QAction("Anomalies", self)
        self._stop_sig_monitor = QAction("Signatures", self)
        self._logs_menu = QMenu("View...")
        self._show_anom_dash = QAction("Anomalies Dashboard", self)
        self._show_sig_dash = QAction("Signatures Dashboard", self)
        self._show_log_dash = QAction("Logs Dashboard", self)

        self._tool_bar = QToolBar("Shortcuts")
        self.addToolBar(self._tool_bar)

        home_icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DesktopIcon)
        self._home_action = QAction(home_icon, "Menu Action", self)
        self._tool_bar.addAction(self._home_action)
        
        self._home_action.triggered.connect(self.show_main_dashboard)

        self._anomaly_dash = AnomalyDashboard()
        self._signature_dash = SignatureDashboard()

    def _setup_gui(self):
        self._board_layout.addWidget(self._cards[0], 0, 0)
        self._board_layout.addWidget(self._cards[1], 0, 1)
        self._board_layout.addWidget(self._cards[2], 1, 0)
        self._board_layout.addWidget(self._cards[3], 1, 1)

        font = self._section_label.font()
        font.setPointSize(28)
        self._section_label.setFont(font)

        self._main_layout.addWidget(self._section_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self._main_layout.addLayout(self._board_layout, 1, 0)

        self._main_dash.setLayout(self._main_layout)
        self._current_central_widget = self._main_dash
        self.setCentralWidget(self._current_central_widget)

        self._set_menus()

    def _set_menus(self):
        self._file_menu.addAction(self._exit_action)

        self._start_monitor_menu.addAction(self._start_anom_monitor)
        self._start_monitor_menu.addAction(self._start_sig_monitor)
        self._tool_menu.addMenu(self._start_monitor_menu)
        self._stop_monitor_menu.addAction(self._stop_anom_monitor)
        self._stop_monitor_menu.addAction(self._stop_sig_monitor)
        self._tool_menu.addMenu(self._stop_monitor_menu)
        self._tool_menu.addSeparator()
        self._logs_menu.addAction(self._show_anom_dash)
        self._logs_menu.addAction(self._show_sig_dash)
        self._logs_menu.addAction(self._show_log_dash)
        self._tool_menu.addMenu(self._logs_menu)

    def _init_window_dimensions(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width() - 70
        screen_height = screen_geometry.height() - 100

        self.setFixedSize(screen_width, screen_height)

    def _run_login(self):
        accept = 1
        reject = 0
        result = self._loginDialog.exec()
        if result == accept:
            print("Logged in")
        elif result == reject:
            sys.exit(1)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
