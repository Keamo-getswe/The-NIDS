import requests
import pandas as pd
from PySide6 import QtCore
from logconfig import logger
import json

class Director:
    def __init__(self):
        self.__pipelineA_url = 'http://localhost:5000/pipelineA/predict'
        self.__pipelineB_url = 'http://localhost:5000/pipelineB/predict'

    @QtCore.Slot()
    def run_pipeline(self, data, name):
        if name == "Pipeline A":
            prediction = self.__request_pipelineA(data)
        else:
            prediction = self.__request_pipelineB(data)

        return prediction

    def __request_pipelineA(self, data):
        data_json = data.to_json(orient='records') 
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.__pipelineA_url, json=data_json, headers=headers)

        if response.status_code == 200:
            return response.json()
        #Log errors for failures gracefully if failed
        
    def __request_pipelineB(self, data):
        array = data.tolist()
        data_json = json.dumps(array)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.__pipelineB_url, json=data_json, headers=headers)

        if response.status_code == 200:
            return response.json()