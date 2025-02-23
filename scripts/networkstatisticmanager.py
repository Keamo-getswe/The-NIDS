from PySide6 import QtCore
from PySide6.QtCore import QObject, QThread
import pandas as pd

class NetworkStatisticManager(QObject):
    data_available = QtCore.Signal(object)
    new_figure_data = QtCore.Signal(object, str)
    
    def __init__(self):
        super().__init__()
        self._data = None
        self._startup_counter = 1

    @QtCore.Slot()
    def add_new_data(self, row):
        # self._mutex.lock()
        if self._data is None:
            self._data = pd.DataFrame(row)
            self._data = self._data.T
            return
        self._data.loc[len(self._data)] = row
        # self._mutex.unlock()
        # if not self._startup_counter == -1:
        if self._startup_counter < 5:
            self._startup_counter += 1
        else:
            self.data_available.emit(self._data)
            self._startup_counter = 1
    
    @QtCore.Slot()
    def handle_request_new_figure_data(self, str):
        if str == "Total Packets":
            y = self.get_total_packets()
            self.new_figure_data.emit(y)
        elif str == "Protocol Distribution":
            pass

    def get_total_packets(self):
        self._mutex.lock()
        total_packets = pd.concat([self._data.iloc[:,2], self._data.iloc[:,3]], axis=1)
        self._mutex.unlock()
        return total_packets

    def get_protocol_distribution(self):
        protocol_distribution = self._data[:,0].value_counts()
        return protocol_distribution