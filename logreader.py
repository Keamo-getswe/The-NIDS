from logconfig import logger
from PySide6.QtCore import QMutex

class LogReader:
    def __init__(self):
        self.file_path = "C:\\Users\\morob\\Documents\\Work\\Honours Project\\The-NIDS\\app.log"
        self.mutex = QMutex()

    def read(self):
        data = ""
        self.mutex.lock
        try:
            with open(self.file_path, "r") as file:
                data = file.read()
        except FileNotFoundError:
            logger.error("The file does not exist.")
        except IOError:
            logger.error("An I/O error occurred while handling the file.")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        finally:
            self.mutex.unlock()

        return data