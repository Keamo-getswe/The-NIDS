from PySide6 import QtCore, QtNetwork
from PySide6.QtCore import QCoreApplication, QByteArray
from PySide6.QtNetwork import QTcpServer, QTcpSocket, QHostAddress
import pandas as pd
import sys
from filereader import FileReader

def override(method):
    return method

class FlowCaptureEngine(QTcpServer):
    def __init__(self):
        super().__init__()
        self.client_socket = None
        # Redacted path
        self.reader = FileReader()
        self.data = self.reader.read_file("CSE-CIC-IDS2018.csv")
        self.count = 0
    
    @override
    def incomingConnection(self, handle):
         if self.client_socket is None:
            self.client_socket = QTcpSocket()
            self.client_socket.setSocketDescriptor(handle)

            self.client_socket.readyRead.connect(self.read_data)
            self.client_socket.disconnected.connect(self.client_disconnected)
            print("Client connected")
            self.client_socket.flush()
    
    @QtCore.Slot()
    def read_data(self):
        if self.client_socket.bytesAvailable():
            request = self.client_socket.readAll().data().decode('utf-8')
            if request == 'START\n':
                self.send_data()
            elif request == 'STOP\n':
                self.client_socket.close()
                self.close()
            else:
                self.client_socket.write(b"Command not allowed. Goodbye.")
                self.client_socket.flush()
                self.client_socket.close()
                self.close()

    @QtCore.Slot()
    def client_disconnected(self):
        print("Client disconnected")
        self.client_socket = None
        self.current_row = 0
        print("Goodbye")
        self.close()
        sys.exit(0)

    def send_data(self):
        if self.count < self.data.shape[0]:
            byte_stream = self.data.iloc[self.count].to_string(header=False, index=False).replace("\n", ",").replace(" ", "") 
            self.client_socket.write(QByteArray(byte_stream+"\n"))
            self.client_socket.flush()
            self.count = self.count+1
        else:
            self.client_socket.write(QByteArray(b'END\n'))
            self.client_socket.flush()
            self.close()

if __name__ == "__main__":
    app = QCoreApplication(sys.argv)
    server = FlowCaptureEngine()
    if not server.listen(QHostAddress("127.0.0.1"), 333):
        print("Server could not start")
        sys.exit(1)
    print("Server started")
    sys.exit(app.exec())