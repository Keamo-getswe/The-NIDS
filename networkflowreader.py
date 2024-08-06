from PySide6 import QtCore
from PySide6.QtCore import QObject, QCoreApplication
from PySide6.QtNetwork import QTcpSocket
import sys

class NetworkFlowReader(QObject):
    data_received = QtCore.Signal(str)
    finished = QtCore.Signal()

    def __init__(self):
        super().__init__()

    @QtCore.Slot()
    def start_data_flow(self):
        self.socket = QTcpSocket()
        self.socket.connectToHost('127.0.0.1', 333)
        if not self.socket.waitForConnected(5000):
            print("Connection failed")
            return
        print("Connected")
        self.socket.readyRead.connect(self.read_data)
        self.socket.write(b'START\n')
        self.socket.flush()
        return

    @QtCore.Slot()
    def stop_data_flow(self):
        self.socket.write(b'STOP\n')
        self.socket.flush()
        self.socket.disconnectFromHost()
        self.finished.emit()

    def request_next_row(self):
        self.socket.write(b'START\n')
        self.socket.flush()

    @QtCore.Slot()
    def read_data(self):
        while self.socket.bytesAvailable():
            data = self.socket.readAll().data().decode('utf-8')
            if data == "END\n":
                self.socket.disconnectFromHost()
                self.finished.emit()
                break
            else:
                self.data_received.emit(data)
                self.request_next_row()
    
