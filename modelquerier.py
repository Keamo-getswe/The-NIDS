from PySide6 import QtCore 
from PySide6.QtCore import QObject, QThread, QDateTime
from agent import Agent
from director import Director
from logconfig import logger
from networkstatisticmanager import NetworkStatisticManager
import sys

class ModelQuerier(QObject):
    alert = QtCore.Signal()
    stopped = QtCore.Signal()
    which_pipeline = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self._agent = Agent(False)
        self._director = Director()
        self.preprocess_started = False
        self.hasStopped = None
        self.pipeline_name = "Pipeline A"
        self.isLogged = None

    @QtCore.Slot()
    def handle_flow_data(self, data):
        if not self.hasStopped:
            if not self.preprocess_started:
                self.preprocess_started = True
                # Necessary for custom handling of fit parameters for feature scaling
                self._agent.prepare_p1_production_preprocess()
                
            if self.pipeline_name == "Pipeline A":
                data = self._agent.p1_production_preprocess(data)
                if data is None:
                    logger.info("Empty data instance in pipeline A model query.")
                    return
            elif self.pipeline_name == "Pipeline B":
                data = self._agent.p2_production_preprocess(data)
                if data is None:
                    logger.info("Empty data instance in pipeline B model query.")
                    return
            
            result = self._director.run_pipeline(data, self.pipeline_name)
            if result[0] == 1:
                    self.alert.emit()
        else:
            if not self.isLogged:
                logger.info("Queries to model halted.")
                self.isLogged = True
                self.stopped.emit()
            
    QtCore.Slot()
    def handle_flow_started(self):
        logger.info("Queries to model initiated.")
        self.hasStopped = False
        self.isLogged = False
        self.which_pipeline.emit()

    @QtCore.Slot()
    def handle_pipeline_signal(self, pipeline):
        self.pipeline_name = pipeline