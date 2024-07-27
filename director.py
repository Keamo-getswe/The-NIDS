import requests
import pandas as pd
from PySide6 import QtCore
import sys

class Director:
    def __init__(self):
        self.__ae_url = 'http://localhost:5000/autoencoder/predict'
        self.__rf_url = 'http://localhost:5000/randomforest/predict'

    @QtCore.Slot()
    def run_pipeline(self, data):
        latent_repr = self.__request_ae_latent_repr(data)
        latent_repr = latent_repr[0]
        prediction = self.__request_rf_predict(latent_repr)
        return prediction

    def __request_ae_latent_repr(self, data):
        data_json = data.to_json(orient='records') 
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.__ae_url, json=data_json, headers=headers)

        if response.status_code == 200:
            return response.json()
    
    def __request_rf_predict(self, data):
        temp = pd.DataFrame(data)
        data_json = temp.to_json(orient='records')
        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.__rf_url, json=data_json, headers=headers)

        if response.status_code == 200:
            return response.json()
        