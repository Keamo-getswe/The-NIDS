import matplotlib
matplotlib.use('Qt5Agg')

from PySide6 import QtCore
from PySide6.QtWidgets import (QGridLayout, QWidget, QLabel,
                               QMessageBox)
from PySide6.QtCore import Qt

import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys

class StatisticsGrapher(QWidget):

    def __init__(self, width=5, height=4, parent=None):
        #Specifying inheritance path
        super(StatisticsGrapher, self).__init__(parent)
        self._has_started = False
        self._init_components(width, height)
        self._setup_gui()
        self.c = 1

    @QtCore.Slot()
    def begin_plotting(self, y, plot):
        self._has_started = True
        if plot == "Total Packets":
            y = pd.concat([y.iloc[:,2],y.iloc[:,3]], axis=1)
            self.plot_bar_graph(y)
            self._main_layout.addWidget(self._canvas1, 0, 0)
        elif plot == "Protocol Distribution":
            sizes = list(y.iloc[:,0].value_counts().values)
            labels = list(y.iloc[:,0].value_counts().index)
            self.plot_pie_chart(labels, sizes)
            self._main_layout.addWidget(self._canvas2, 0, 0) 
        
    def _init_components(self, width, height):
        dots_per_in = 100
        fig1 = Figure(figsize=(width, height), dpi=dots_per_in)
        fig2 = Figure(figsize=(width, height), dpi=dots_per_in)
        self._canvas1 = FigureCanvas(fig1)
        self._canvas2 = FigureCanvas(fig2)
        self.ax1 = self._canvas1.figure.add_subplot(111)
        self.ax2 = self._canvas2.figure.add_subplot(111)
        self._main_layout = QGridLayout()
        self._empty_label = QLabel("Nothing to report")
        
    def _setup_gui(self):
        self._empty_label.setStyleSheet("font-size: 64px; padding: 800px 500px 900px;")
        self._main_layout.addWidget(self._empty_label, 0, 0, Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._main_layout)

    def plot_bar_graph(self, y):
        x = ["Total Forward Packets", "Total Backward Packets"]
        colors = ['red', 'blue']
        if not (y.shape[1] == 2):
            QMessageBox.critical(None, "Inconsistent Data Dimensions.","The input data has more than 2 columns. The plot cannot be completed.")
            return
        totals = y.sum()

        self.ax1.bar(x, totals, color=colors)

        self.ax1.set_title('Total Number of Packets Processed')
        self.ax1.set_xlabel('Categories')
        self.ax1.set_ylabel('Values')
        self._canvas1.draw()

    @QtCore.Slot()
    def change_figure(self, y, graph_type):
        if self._has_started:
            if graph_type == "Total Packets":
                self.ax1.cla()
                y = pd.concat([y.iloc[:,2],y.iloc[:,3]], axis=1)
                self.plot_bar_graph(y)
                self._canvas2.hide()
                self._main_layout.addWidget(self._canvas1, 0, 0)
                self._canvas1.show()
            elif graph_type == "Protocol Distribution":
                self.ax2.cla()
                sizes = list(y.iloc[:,0].value_counts().values)
                labels = list(y.iloc[:,0].value_counts().index)
                self.plot_pie_chart(labels, sizes)
                self._canvas1.hide()
                self._main_layout.addWidget(self._canvas2, 0, 0)
                self._canvas2.show()

    def update_plot(self, data, graph_type):
        if graph_type == "Total Packets":
            self.ax1.cla()
            data = pd.concat([data.iloc[:,2], data.iloc[:,3]], axis=1)
            self.plot_bar_graph(data)
        elif graph_type == "Protocol Distribution":
            self.ax2.cla()
            labels = list(data.iloc[:,0].value_counts().index)
            new_sizes = list(data.iloc[:,0].value_counts().values)
            self.plot_pie_chart(labels, new_sizes)
    
    def plot_pie_chart(self, labels, sizes):
        self.ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

        self.ax2.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        self.ax2.set_title('Protocol Distribution')
        self._canvas2.draw()
