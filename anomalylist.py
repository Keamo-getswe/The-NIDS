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
        self.count = len(self.anomalies)

    def add_anomaly(self, anomaly):
        self.anomalies[f"{self.count}"] = anomaly
        self.count += 1

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

    