import requests
import json
from agent import Agent
from autoencoder import AutoEncoder
import pandas as pd


url = 'http://localhost:5000/randomforest/predict'
agent = Agent("C:\\Users\\morob\\Documents\\Work\\Honours Project\\The-NIDS\\CICIDS2017\\MachineLearningCVE")
_, test_data = agent.preprocess()
p = test_data.iloc[1]
ae = AutoEncoder(5,3)
ae.load_model()
_, pred = ae.encode(p)
temp = pd.DataFrame(pred)
data_json = temp.to_json(orient='records') 
headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=data_json, headers=headers)

if response.status_code == 200:
    predictions = response.json()
    print('Predictions:', predictions[0])
else:
    print('Error:', response.text)
