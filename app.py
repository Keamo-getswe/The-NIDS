from flask import Flask, request, jsonify
import pandas as pd
from autoencoder import AutoEncoder
from randomforest import RandomForest
from utility import AE_FILE_PATH
import ast

app = Flask(__name__)

# Load models
ae = AutoEncoder(5, 3)
ae.load_model()

rf = RandomForest()
rf.load_model()

@app.route('/autoencoder/predict', methods=['POST'])
def ae_predict():
    json_data = request.json
    #Format data to handle request
    data_list = ast.literal_eval(json_data)
    data_point = pd.DataFrame(data_list)

    _, p = ae.encode(data_point.T)
    return jsonify(p.tolist())

@app.route('/randomforest/predict', methods=['POST'])
def rf_predict():
    json_data = request.json
    #Format data to handle request
    data_list = ast.literal_eval(json_data)
    data_point = pd.DataFrame(data_list)

    p = rf.predict(data_point.T)
    return jsonify(p.tolist())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
