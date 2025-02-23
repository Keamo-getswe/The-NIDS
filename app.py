from flask import Flask, request, jsonify
import pandas as pd
from autoencoder import AutoEncoder
from randomforest import RandomForest
from sklearn.decomposition import PCA
from lstmautoencoder import LSTMAutoencoder
import utility
import joblib
import cupy as cp
import numpy as np
import ast
import sys

app = Flask(__name__)

# Load pipeline A models
hidden_dimensions = [utility.HIDDEN_DIMENSION, utility.BOTTLENECK_DIMENSION]
ae = AutoEncoder(utility.INPUT_DIMENSION, hidden_dimensions)
ae.load_model()

rf = RandomForest()
rf.load_model()

# Load pipeline B autoencoder.
# Note: PCA must be used prior to creating sequences for model
# hence it is used as preprocessing step.

lstm_ae = LSTMAutoencoder(training=False)

@app.route('/pipelineA/predict', methods=['POST'])
def p1_predict():
    json_data = request.json
    #Format data to handle request
    data_list = ast.literal_eval(json_data)
    data_list = list(data_list[0].values())
    data_point = pd.DataFrame(data_list)
    gpu_data_point = cp.array(data_point)
    ae.encode(gpu_data_point.T, False)
    latent_space = ae.get_encoded_data()
    latent_space = pd.DataFrame(cp.asnumpy(latent_space))
    prediction = rf.predict(latent_space)
    return jsonify(prediction.tolist())

@app.route('/pipelineB/predict', methods=['POST'])
def p2_predict():
    json_data = request.json
    data_list = ast.literal_eval(json_data)
    data_point = np.array(data_list)
    _,_, anomalies = lstm_ae.predict(data_point)
    return jsonify(anomalies.tolist())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
