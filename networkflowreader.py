from PySide6 import QtCore
from PySide6.QtCore import QObject, QCoreApplication, QThread, QDateTime
from PySide6.QtNetwork import QTcpSocket, QHostAddress
import utility
from logconfig import logger

class NetworkFlowReader(QObject):
    data_received = QtCore.Signal(str)
    finished = QtCore.Signal()
    connection_failed = QtCore.Signal()
    stopped = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.hasEnded = False
    
    @QtCore.Slot()
    def start_data_flow(self):
        self.hasEnded = False
        self.socket = QTcpSocket()
        self.socket.connectToHost(QHostAddress(utility.DESTINATION_IP), utility.PORT)
        if not self.socket.waitForConnected(5000):
            logger.critical("Network flow reader connection to flow engine failed.")
            self.connection_failed.emit()
            return
        logger.info("Network flow reader connection to flow engine successful. Requesting initiation of data flow.")
        self.socket.readyRead.connect(self.read_data, QtCore.Qt.QueuedConnection)
        self.socket.write(b'START\n')
        self.socket.flush()
        return

    @QtCore.Slot()
    def stop_data_flow(self):
        self.socket.write(b'STOP\n')
        logger.info("Network flow reader halted. Disconnecting from host.")
        self.hasEnded = True
        self.socket.flush()
        self.socket.disconnectFromHost()
        self.stopped.emit()

    def request_next_row(self):
        self.socket.write(b'START\n')
        self.socket.flush()

    @QtCore.Slot()
    def read_data(self):
        data = self.socket.readLine().data().decode('utf-8')

        if data == "END\n":
            logger.info("Network flow concluded. Disconnecting from host.")
            self.socket.disconnectFromHost()
            self.finished.emit()
            self.hasEnded = True
        else:
            if not self.hasEnded:
                self.data_received.emit(data)
                self.request_next_row()
    
