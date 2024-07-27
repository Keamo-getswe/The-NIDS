from flask import Flask, request, jsonify
import pandas as pd
from autoencoder import AutoEncoder
from randomforest import RandomForest
import  utility
import ast

app = Flask(__name__)

# Load models
ae = AutoEncoder(utility.INPUT_DIMENSION, utility.HIDDEN_DIMENSION)
ae.load_model()

rf = RandomForest()
rf.load_model()

@app.route('/autoencoder/predict', methods=['POST'])
def ae_predict():
    json_data = request.json
    #Format data to handle request
    data_list = ast.literal_eval(json_data)
    data_point = pd.DataFrame(data_list)

    ae.encode(data_point.T)
    p = ae.get_encoded_data()
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
