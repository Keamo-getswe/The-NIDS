from PySide6 import QtCore
from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QPushButton,
                               QWidget, QGroupBox, QComboBox)
from statisticsmanagerworker import StatisticsManagerWorker
from statisticsgrapher import StatisticsGrapher
from logconfig import logger

class StatisticsDashboard(QWidget):
    request_new_figure_data = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        
        self._init_components()
        self._set_gui()

        self._stats_manager_thread = QThread()
        self._stats_manager_thread.setObjectName("Stats Manager Thread")
        self._manager_worker = StatisticsManagerWorker()
        self._manager_worker.moveToThread(self._stats_manager_thread)

        self._manager_worker._stats_manager.data_available.connect(self.handle_data_available)
        self._refresh_button.clicked.connect(self.handle_refresh)

        self._graph_box.currentTextChanged.connect(self.handle_changed_text)
        self._manager_worker._stats_manager.new_figure_data.connect(self._grapher.change_figure)
        
        self._stats_manager_thread.start()

    @QtCore.Slot()
    def handle_refresh(self):
        pass

    @QtCore.Slot()
    def handle_changed_text(self, str):
        data = self._manager_worker._stats_manager._data
        self._manager_worker._stats_manager.new_figure_data.emit(data, str)
        self._new_figure_name = str

    @QtCore.Slot()
    def handle_data_available(self, data):
        if self._grapher._has_started == False:
            self._grapher.begin_plotting(data, self._graph_box.currentText())
            self._grapher._has_started = True
        else:
            self._grapher.update_plot(data, self._graph_box.currentText())

    def _init_components(self):
        self._section_label = QLabel("Statistics Dashboard")
        self._new_data_label = QLabel("")
        self._refresh_button = QPushButton("Refresh")
        self._stats_display_label = QLabel("Display:")
        self._graph_box = QComboBox()

        self._button_layout = QHBoxLayout()
        self._tool_layout = QHBoxLayout()
        self._combo_layout = QVBoxLayout()
        self._main_layout = QVBoxLayout()
        self._button_group = QGroupBox()
        self._combo_group = QGroupBox()
        self._grapher = StatisticsGrapher(8, 7)
        self._new_figure_name = ""

        self._button_layout.setStretch(0, 1)
        self._button_layout.setStretch(1, 1)

        self._graph_box.addItem("Total Packets")
        self._graph_box.addItem("Protocol Distribution")
        self._graph_box.setEditable(False)

    def _set_gui(self):
        button_width = 75
        button_height = 25
        button_group_width = 280
        button_group_height = 90
        combo_box_width = 150
        combo_box_height = 25

        self._refresh_button.setFixedSize(button_width, button_height)
        self._graph_box.setFixedSize(combo_box_width, combo_box_height)

        self._button_layout.addWidget(self._refresh_button)
        self._combo_layout.addWidget(self._stats_display_label)
        self._combo_layout.addWidget(self._graph_box)
        self._combo_group.setLayout(self._combo_layout)
        self._button_layout.addWidget(self._combo_group)

        self._button_group.setLayout(self._button_layout)
        self._button_group.setFixedSize(button_group_width, button_group_height)
        self._tool_layout.addWidget(self._button_group)
        self._tool_layout.addWidget(self._new_data_label)
        
        font = self._section_label.font()
        font.setPointSize(28)
        self._section_label.setFont(font)

        font = self._new_data_label.font()
        font.setPointSize(16)
        self._new_data_label.setFont(font)
        
        self._main_layout.addWidget(self._section_label, 1, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop)
        self._main_layout.addLayout(self._tool_layout)
        self._main_layout.addWidget(self._grapher)

        self.setLayout(self._main_layout)
        