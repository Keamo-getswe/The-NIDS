from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QLabel, QApplication, QGridLayout,
                               QWidget, QMenu, QToolBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from cardwidget import CardWidget
from anomalydashboard import AnomalyDashboard
from logdashboard import LogDashboard
from statisticsdashboard import StatisticsDashboard
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self._init_components()
        self._setup_gui()
        self._init_window_dimensions()

        self._cards[0].clicked.connect(self.show_anomaly_dashboard)

        self._anomaly_dash.new_model_data.connect(self._stats_dash._manager_worker._stats_manager.add_new_data)
        self._cards[1].clicked.connect(self.show_statistics_dashboard)
        self._cards[2].clicked.connect(self.show_log_dashboard)
        self.setWindowTitle("The NIDS")

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
    def show_log_dashboard(self):
        self.set_central(self._log_dash)

    @QtCore.Slot()
    def show_statistics_dashboard(self):
        self.set_central(self._stats_dash)

    def _init_components(self):
        # Redacted
        icon_path = "images\\"
        self._cards = []
        icon_names = [
            "anonymous-user-icon.png",
            "column-chart-icon.png",
            "writing-icon.png"
        ]
        card_titles = [
            "Anomalies",
            "Statistics",
            "Logs"
        ]

        for i in range(3):
            self._cards += [CardWidget(icon_names[i], card_titles[i])]

        self._board_layout = QGridLayout()
        self._main_layout = QGridLayout()
        self._main_dash = QWidget()
        self._section_label = QLabel("Main Dashboard")

        self._file_menu = self.menuBar().addMenu("File")
        self._exit_action = QAction("Exit", self)

        self._tool_menu = self.menuBar().addMenu("Tools")
        self._start_anom_monitor = QAction("Start Monitoring...", self)
        self._stop_anom_monitor = QAction("Stop Monitoring...", self)

        self._logs_menu = self.menuBar().addMenu("View")
        self._show_stats_dash = QAction("Statistics Dashboard", self)
        self._show_log_dash = QAction("Logs Dashboard", self)

        self._tool_bar = QToolBar("Shortcuts")
        self.addToolBar(self._tool_bar)

        self._home_action = QAction(QIcon(icon_path+"home-icon.png"), "Menu Action", self)
        self._tool_bar.addAction(self._home_action)
        self._anomaly_action = QAction(QIcon(icon_path+"anomaly-icon.png"), "Anomaly Action", self)
        self._tool_bar.addAction(self._anomaly_action)
        self._stats_action = QAction(QIcon(icon_path+"stats-icon.png"), "Statistics Action", self)
        self._tool_bar.addAction(self._stats_action)
        self._log_action = QAction(QIcon(icon_path+"log-icon.png"), "Log Action", self)
        self._tool_bar.addAction(self._log_action)
        
        self._show_log_dash.triggered.connect(self.show_log_dashboard)
        self._show_stats_dash.triggered.connect(self.show_statistics_dashboard)
        self._exit_action.triggered.connect(self.close)

        self._anomaly_dash = AnomalyDashboard()
        self._log_dash = LogDashboard()
        self._stats_dash = StatisticsDashboard()

    def _setup_gui(self):
        self._board_layout.addWidget(self._cards[0], 0, 0)
        self._board_layout.addWidget(self._cards[1], 0, 1)
        self._board_layout.addWidget(self._cards[2], 1, 0)

        font = self._section_label.font()
        font.setPointSize(28)
        self._section_label.setFont(font)

        self._main_layout.addWidget(self._section_label, 0, 0, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self._main_layout.addLayout(self._board_layout, 1, 0)

        self._main_dash.setLayout(self._main_layout)
        self._current_central_widget = self._main_dash
        self.setCentralWidget(self._current_central_widget)

        self._set_menus()
        self._set_toolbar()

    def _set_menus(self):
        self._file_menu.addAction(self._exit_action)

        self._tool_menu.addAction(self._start_anom_monitor)
        self._tool_menu.addAction(self._stop_anom_monitor)
        self._tool_menu.addSeparator()
        self._logs_menu.addAction(self._show_log_dash)

        self._logs_menu.addAction(self._show_log_dash)
        self._logs_menu.addAction(self._show_stats_dash)
        
        self._start_anom_monitor.triggered.connect(self._anomaly_dash.start_monitoring)
        self._stop_anom_monitor.triggered.connect(self._anomaly_dash.stop_monitoring)

    def _set_toolbar(self):
        self._home_action.triggered.connect(self.show_main_dashboard)
        self._anomaly_action.triggered.connect(self.show_anomaly_dashboard)
        self._stats_action.triggered.connect(self.show_statistics_dashboard)
        self._log_action.triggered.connect(self.show_log_dashboard)

    def _init_window_dimensions(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        screen_width = screen_geometry.width() - 70
        screen_height = screen_geometry.height() - 100

        self.setFixedSize(screen_width, screen_height)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
