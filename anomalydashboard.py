from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import (QWidget, QPushButton, QComboBox,
                               QHeaderView, QGroupBox, QHBoxLayout, 
                               QVBoxLayout, QGridLayout,QLabel,
                               QTableView, QRadioButton)
from PySide6.QtCore import QDateTime, Qt, QThread, QObject
from networkflowreader import NetworkFlowReader
from anomaly import Anomaly
from anomalymodel import AnomalyModel
from filterproxymodel import FilterProxyModel
from anomalylist import AnomalyList
from modelquerier import ModelQuerier
import sys

class AnomalyDashboard(QWidget):
    flow_thread_stopped = QtCore.Signal()
    model_query_thread_stopped = QtCore.Signal()
    send_requested_pipeline = QtCore.Signal(str)
    new_model_data = QtCore.Signal(list)

    def __init__(self):
        super().__init__()
        self._anom_detection_started = False
        self.preprocess_started = False

        self._init_components()
        self._setup_gui()

        self._start_button.clicked.connect(self.start_monitoring)
        self._start_button.clicked.connect(self.disable_other_pipeline)
        self._duration_filters.currentTextChanged.connect(self.proxy_model.handle_new_filter)
        self.pipeline_buttons[0].toggled.connect(self.handle_which_pipeline)
        self.pipeline_buttons[1].toggled.connect(self.handle_which_pipeline)
        self.send_requested_pipeline.connect(self.anomaly_model.change_pipeline)

    @QtCore.Slot()
    def start_monitoring(self):
        if not self._anom_detection_started:
            QThread.currentThread().setObjectName("Main Thread")
            self.flow_engine_thread = QThread()
            self.flow_engine_thread.setObjectName("Flow Engine Thread")
            self.flow_engine_worker = NetworkFlowReader()
            self.flow_engine_worker.moveToThread(self.flow_engine_thread)
            self.model_query_thread = QThread()
            self.model_query_thread.setObjectName("Model Query Thread")
            self.model_query_worker = ModelQuerier()
            self.model_query_worker.moveToThread(self.model_query_thread)    

            self.flow_engine_thread.started.connect(self.flow_engine_worker.start_data_flow)
            self.model_query_thread.started.connect(self.model_query_worker.handle_flow_started)
            self._stop_button.clicked.connect(self.flow_engine_worker.stop_data_flow)
            self.flow_engine_worker.stopped.connect(self.flow_engine_thread.quit)

            self._stop_button.clicked.connect(self.stop_monitoring)
            self.model_query_worker.stopped.connect(self.model_query_thread.quit)

            self.flow_engine_worker.data_received.connect(self.model_query_worker.handle_flow_data)
            self.flow_engine_worker.connection_failed.connect(self.handle_failed_flow_connection)

            self.model_query_worker.which_pipeline.connect(self.handle_which_pipeline)
            self.send_requested_pipeline.connect(self.model_query_worker.handle_pipeline_signal)
            self.model_query_worker.alert.connect(self.addAnomaly)
            self.model_query_worker._agent.new_data.connect(self.forward_data)

            self.flow_engine_thread.start()
            self.model_query_thread.start()
            self._anom_detection_started = True

    def stop_monitoring(self):
        self.model_query_worker.hasStopped = True
        self._anom_detection_started = False
        if self.pipeline_buttons[0].isChecked():
            self.pipeline_buttons[1].setDisabled(False)
        else:
            self.pipeline_buttons[0].setDisabled(False)

    @QtCore.Slot()
    def handle_failed_flow_connection(self):
        self.flow_engine_thread.quit()
        self.model_query_thread.quit()
        self._anom_detection_started = False
        #Call logger

    @QtCore.Slot()
    def handle_which_pipeline(self):
        for button in self.pipeline_buttons:
            if button.isChecked():
                self.send_requested_pipeline.emit(button.text())

    @QtCore.Slot()
    def addAnomaly(self):
        #Consider adding QMutex for read/write protection
        row = self._anomaly_table.model().rowCount()
        self._anomaly_table.model().sourceModel().insertRow(row)
        #Update model
        self.proxy_model.invalidateFilter()

    @QtCore.Slot()
    def disable_other_pipeline(self):
        if self.pipeline_buttons[0].isChecked():
            self.pipeline_buttons[1].setDisabled(True)
        elif self.pipeline_buttons[1].isChecked():
            self.pipeline_buttons[0].setDisabled(True)

    @QtCore.Slot()
    def forward_data(self, data):
        self.new_model_data.emit(data)
    
    def _init_components(self):
        self._start_button = QPushButton("Start")
        self._stop_button = QPushButton("Stop")
        self._duration_filters = QComboBox()
        self._anomaly_table = QTableView()

        self._main_layout = QGridLayout()
        self._button_layout = QHBoxLayout()
        self._radio_button_layout = QVBoxLayout()
        self._pipelineA_layout = QHBoxLayout()
        self._pipelineB_layout = QHBoxLayout()
        self._combo_layout = QVBoxLayout()

        self._button_group = QGroupBox()
        self._combo_group = QGroupBox()
        self.pipeline_buttons = []

        self._filters_label = QLabel("Filter By:")
        self._section_label = QLabel("Anomalies Dashboard")

        self._duration_filters.addItem("None")
        self._duration_filters.addItem("Last Hour")
        self._duration_filters.addItem("Last Day")
        self._duration_filters.addItem("Last Month")
        self._duration_filters.setEditable(False)

        self.pipelineA_button = QRadioButton()
        self.pipelineA_button.setText("Pipeline A")
        self.pipelineA_button.setChecked(True)
        self.pipeline_buttons.append(self.pipelineA_button)
        
        self.pipelineB_button = QRadioButton()
        self.pipelineB_button.setText("Pipeline B")
        self.pipeline_buttons.append(self.pipelineB_button)
        
        self.anomaly_model = AnomalyModel()
        self.proxy_model = FilterProxyModel()
        self.proxy_model.setSourceModel(self.anomaly_model)
        self._anomaly_table.setModel(self.proxy_model)

    def _setup_gui(self):
        button_width = 75
        button_height = 25
        button_group_width = 400

        self._start_button.setFixedSize(button_width, button_height)
        self._stop_button.setFixedSize(button_width, button_height)

        self._button_layout.addWidget(self._start_button)
        self._button_layout.addWidget(self._stop_button)

        self._combo_layout.addWidget(self._filters_label)
        self._combo_layout.addWidget(self._duration_filters)
        self._combo_group.setLayout(self._combo_layout)
        self._button_layout.addWidget(self._combo_group)

        self._pipelineA_layout.addWidget(self.pipeline_buttons[0])
        self._pipelineB_layout.addWidget(self.pipeline_buttons[1])
        self._radio_button_layout.addLayout(self._pipelineA_layout)
        self._radio_button_layout.addLayout(self._pipelineB_layout)
        self._button_layout.addLayout(self._radio_button_layout)

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