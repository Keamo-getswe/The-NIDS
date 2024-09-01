from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import (QWidget, QPushButton, QComboBox,
                               QHeaderView, QGroupBox, QHBoxLayout, 
                               QVBoxLayout, QGridLayout,QLabel,
                               QTableView)
from PySide6.QtCore import QDateTime, Qt, QThread
from networkflowreader import NetworkFlowReader
from agent import Agent
from director import Director
from anomalymodel import AnomalyModel
from anomalylist import AnomalyList
import sys

class AnomalyDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self._agent = Agent()
        self._director = Director()
        self._anom_detection_started = False
        self.preprocess_started = False

        self._init_components()
        self._setup_gui()

        self._start_button.clicked.connect(self.start_monitoring)

    @QtCore.Slot()
    def start_monitoring(self):
        if not self._anom_detection_started:
            self.thread = QThread()
            self.worker = NetworkFlowReader()
            self.worker.moveToThread(self.thread)
            
            self.thread.started.connect(self.worker.start_data_flow)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.worker.data_received.connect(self.handle_flow_data)
            
            self.thread.start()
            self._anom_detection_started = True

    def stop_monitoring(self):
        pass

    def show_last_hour_anomalies(self):
        pass

    def show_last_day_anomalies(self):
        pass

    def show_last_month_anomalies(self):
        pass

    @QtCore.Slot()
    def addAnomaly(self, timestamp):
        pass
        
    @QtCore.Slot()
    def handle_flow_data(self, data):
        if not self.preprocess_started:
            self.preprocess_started = True
            self._agent.prepare_production_preprocess()

        data = self._agent.production_preprocess(data)
        result = self._director.run_pipeline(data)
        if result[0] == 1:
            self.addAnomaly()
    
    def _init_components(self):
        self._start_button = QPushButton("Start")
        self._stop_button = QPushButton("Stop")
        self._duration_filters = QComboBox()
        self._filter_button = QPushButton("Filter")
        self._anomaly_table = QTableView()

        self._main_layout = QGridLayout()
        self._button_layout = QHBoxLayout()
        self._filter_layout = QHBoxLayout()
        self._combo_layout = QVBoxLayout()

        self._button_group = QGroupBox()
        self._combo_group = QGroupBox()

        self._filters_label = QLabel("Filter By:")
        self._section_label = QLabel("Anomalies Dashboard")

        self._duration_filters.addItem("Last Hour")
        self._duration_filters.addItem("Last Day")
        self._duration_filters.addItem("Last Month")
        
        anomaly_model = AnomalyModel()
        self._anomaly_table.setModel(anomaly_model)

    def _setup_gui(self):
        button_width = 75
        button_height = 25
        button_group_width = 400

        self._start_button.setFixedSize(button_width, button_height)
        self._stop_button.setFixedSize(button_width, button_height)
        self._filter_button.setFixedSize(button_width, button_height)

        self._button_layout.addWidget(self._start_button)
        self._button_layout.addWidget(self._stop_button)

        self._combo_layout.addWidget(self._filters_label)
        self._filter_layout.addWidget(self._duration_filters)
        self._filter_layout.addWidget(self._filter_button)
        self._combo_layout.addLayout(self._filter_layout)
        self._combo_group.setLayout(self._combo_layout)

        self._button_layout.addWidget(self._combo_group)
        self._button_group.setLayout(self._button_layout)
        self._button_group.setFixedWidth(button_group_width)

        self._anomaly_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self._anomaly_table.verticalHeader().setVisible(False)

        font = self._section_label.font()
        font.setPointSize(28)
        self._section_label.setFont(font)

        self._main_layout.addWidget(self._section_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self._main_layout.addWidget(self._button_group, 1, 0)
        self._main_layout.addWidget(self._anomaly_table, 2, 0)
        self.setLayout(self._main_layout)