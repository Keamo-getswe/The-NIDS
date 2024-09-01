import requests
import pandas as pd
from PySide6 import QtCore
import sys

class Director:
    def __init__(self):
        self.__pipelineA_url = 'http://localhost:5000/pipelineA/predict'

    @QtCore.Slot()
    def run_pipeline(self, data):
        prediction = self.__request_pipelineA(data)
        return prediction

    def __request_pipelineA(self, data):
        data_json = data.to_json(orient='records') 
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.__pipelineA_url, json=data_json, headers=headers)

        if response.status_code == 200:
            return response.json()
        