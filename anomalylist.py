from PySide6 import QtCore
from PySide6.QtCore import QMutex, QMutexLocker, QDateTime
from anomaly import Anomaly

class AnomalyListMeta(type):
    _instances = {}
    _mutex = QMutex()
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with QMutexLocker(cls._mutex):
                if cls not in cls._instances:
                    cls._instances[cls] = super(AnomalyListMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class AnomalyList(metaclass=AnomalyListMeta):
    def __init__(self):
        self.anomalies = {}

    def add_anomaly(self, anomaly):
        self.anomalies[anomaly.get_timestamp().toString("yyyy-MM-dd HH:mm:ss")] = anomaly

    def get_anomaly(self, id):
        if len(self.anomalies) > 0:
            if id in list(self.anomalies.keys()):
                return self.anomalies[id]
            else:
                return None
        else:
                return None

    def get_anomaly_list(self):
        return self.anomalies    

    