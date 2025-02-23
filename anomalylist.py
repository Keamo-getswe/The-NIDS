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
        self.a_anomalies = {}
        self.b_anomalies = {}
        self.a_count = len(self.a_anomalies)
        self.b_count = len(self.b_anomalies)

    def add_anomaly(self, anomaly, type):
        if type == "Pipeline A":
            self.a_anomalies[f"{self.a_count}"] = anomaly
            self.a_count += 1
        elif type == "Pipeline B":
            self.b_anomalies[f"{self.b_count}"] = anomaly
            self.b_count += 1

    def get_anomaly(self, id, type):
        if type == "Pipeline A":
            if len(self.a_anomalies) > 0:
                if id in list(self.a_anomalies.keys()):
                    return self.a_anomalies[id]
                else:
                    return None
            else:
                    return None
        elif type == "Pipeline B":
            if len(self.b_anomalies) > 0:
                if id in list(self.b_anomalies.keys()):
                    return self.b_anomalies[id]
                else:
                    return None
            else:
                    return None
    
    def get_a_count(self):
        return self.a_count
    
    def get_b_count(self):
        return self.b_count
    
    def get_total_count(self):
        return self.get_a_count() + self.get_b_count()

    def get_a_anomaly_list(self):
        return self.a_anomalies
    
    def get_b_anomaly_list(self):
        return self.b_anomalies
