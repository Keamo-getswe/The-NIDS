from PySide6 import QtCore
from PySide6.QtCore import QSortFilterProxyModel, QDateTime

class FilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.filter = "None"
        self.current_date_time = QDateTime().currentDateTime()

    @QtCore.Slot()
    def handle_new_filter(self, text):
        self.filter = text
        self.current_date_time = QDateTime().currentDateTime()

    def filterAcceptsRow(self, source_row, source_parent):
        if self.filter == "None":
            return True
        else:
            index = self.sourceModel().index(source_row, 1, source_parent)
            date_data = self.sourceModel().data(index)
            if (self.filter == "Last Hour"):
                if self.current_date_time.addSecs(-3600) <= date_data <= self.current_date_time:
                    return True
            if (self.filter == "Last Day"):
                if self.current_date_time.addDays(-1) <= date_data <= self.current_date_time:
                    return True
            if (self.filter == "Last Month"):
                if self.current_date_time.addMonths(-1) <= date_data <= self.current_date_time:
                    return True
        return False