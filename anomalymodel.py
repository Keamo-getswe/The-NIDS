from PySide6 import QtCore
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from anomalylist import AnomalyList
from anomaly import Anomaly

class AnomalyModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pipeline_name = "PipeLine A"

    @QtCore.Slot()
    def change_pipeline(self, pipeline):
        self.beginResetModel()
        self.pipeline_name = pipeline
        self.endResetModel()

    def rowCount(self, parent=None):
        if self.pipeline_name == "Pipeline A":    
            return AnomalyList().get_a_count()   
        return AnomalyList().get_b_count()

    def columnCount(self, parent=None):
            return 7

    def data(self, index, role = Qt.DisplayRole):
        if not (index.isValid()):
            return None
        
        if (index.row() >= self.rowCount() or index.row() < 0):
            return None
        
        if (index.column() >= self.columnCount() or index.column() < 0):
            return None

        if role == Qt.DisplayRole:
            if (self.pipeline_name == "Pipeline A"):
                if (len(AnomalyList().a_anomalies) == 0):
                    return None
            elif (self.pipeline_name == "Pipeline B"):
                if (len(AnomalyList().b_anomalies) == 0):
                    return None
            
            col = index.column()    
            anomaly = AnomalyList().get_anomaly(str(index.row()), self.pipeline_name)
            if not (anomaly == None):
                if (col == 0):
                    return anomaly.get_id()
                elif (col == 1):
                    return anomaly.get_timestamp()
                elif (col == 2):
                    return anomaly.get_source_ip()
                elif (col == 3):
                    return anomaly.get_source_port()
                elif (col == 4):
                    return anomaly.get_destination_ip()
                elif (col == 5):
                    return anomaly.get_destination_port()
                elif (col == 6):
                    return anomaly.get_action()
            else:
                return None

        return None

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return ["ID", "Timestamp", "SrcIP", "SrcPort", "DestIP", "DestPort", "Action"][section]
        return None
    
    def insertRow(self, position, index=QModelIndex()):
        self.insertRows(position, 1, index)
    
    def insertRows(self, position, rows, parent):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        pipeline = self.pipeline_name
        for row in range(rows):
            anomaly = Anomaly()
            anomaly.set_timestamp()
            if pipeline == "Pipeline A":
                anomaly.set_id(AnomalyList().get_a_count())
            elif pipeline == "Pipeline B":
                anomaly.set_id(AnomalyList().get_b_count())
            AnomalyList().add_anomaly(anomaly, pipeline)
        self.endInsertRows()
        return True