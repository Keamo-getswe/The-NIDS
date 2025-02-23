from PySide6 import QtCore
from PySide6.QtCore import QDateTime
import utility

class Anomaly:
    def __init__(self):
        self.id = None
        self.timestamp = None
        self.source_ip = utility.SOURCE_IP
        self.destination_ip = utility.DESTINATION_IP
        self.source_port = utility.PORT
        self.destination_port = utility.PORT
        self.action = "Alert"

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id
    
    def get_source_ip(self):
        return self.source_ip
    
    def set_source_ip(self, src_ip):
        self.source_ip = src_ip
    
    def get_source_port(self):
        return self.source_port
    
    def set_source_port(self, src_prt):
        self.source_port = src_prt
    
    def get_destination_ip(self):
        return self.destination_ip
    
    def set_destination_ip(self, dest_ip):
        self.destination_ip = dest_ip
    
    def get_destination_port(self):
        return self.destination_port
    
    def get_timestamp(self):
        if (self.timestamp == None):
            self.set_timestamp()
        return self.timestamp
    
    def set_timestamp(self):
            self.timestamp = QDateTime.currentDateTime()
    
    def get_action(self):
        return self.action
    
    