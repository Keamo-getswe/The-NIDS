from flask import Flask, request, jsonify
import pandas as pd
from autoencoder import AutoEncoder
from randomforest import RandomForest
import  utility
import cupy as cp
import ast
import sys

app = Flask(__name__)

# Load models
hidden_dimensions = [utility.HIDDEN_DIMENSION, utility.BOTTLENECK_DIMENSION]
ae = AutoEncoder(utility.INPUT_DIMENSION, hidden_dimensions)
ae.load_model()

rf = RandomForest()
rf.load_model()

@app.route('/pipelineA/predict', methods=['POST'])
def ae_predict():
    json_data = request.json
    #Format data to handle request
    data_list = ast.literal_eval(json_data)
    data_list = list(data_list[0].values())
    data_point = pd.DataFrame(data_list)
    gpu_data_point = cp.array(data_point)
    ae.encode(gpu_data_point.T)
    latent_space = ae.get_encoded_data()
    latent_space = pd.DataFrame(cp.asnumpy(latent_space))
    prediction = rf.predict(latent_space)
    return jsonify(prediction.tolist())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
