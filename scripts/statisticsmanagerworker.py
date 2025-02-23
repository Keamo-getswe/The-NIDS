from PySide6 import QtCore
from PySide6.QtCore import QObject, QThread
from networkstatisticmanager import NetworkStatisticManager


class StatisticsManagerWorker(QObject):

    def __init__(self):
        super().__init__()
        self._stats_manager = NetworkStatisticManager()
