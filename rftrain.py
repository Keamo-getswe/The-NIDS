from randomforest import RandomForest
from autoencoder import AutoEncoder
from sklearn.metrics import accuracy_score, confusion_matrix
import cupy as cp
import numpy as np
import joblib
import utility
import os

def train_and_save_model():
    train_data = data["train_data"]
    ae.encode(cp.array(train_data.to_numpy()), False)
    reduced_features = ae.get_encoded_data()
    train_labels = data["train_labels"]
    reduced_features = cp.asnumpy(reduced_features)
    rf.train(reduced_features, train_labels)
    rf.save_model()

if __name__ == "__main__":
    rf = RandomForest()
    input_size = utility.INPUT_DIMENSION
    hidden_size = [utility.HIDDEN_DIMENSION, utility.BOTTLENECK_DIMENSION]
    ae = AutoEncoder(input_size, hidden_size)
    ae.load_model()
    data = joblib.load(utility.P1_TRAIN_TEST_DATA_PATH)
    train_and_save_model()
    test_data = data["test_data"]
    ae.encode(cp.array(test_data.to_numpy()))
    reduced_features = ae.get_encoded_data()
    reduced_features = cp.asnumpy(reduced_features)
    y = rf.predict(reduced_features)
    threshold = 0.9
    y = (y[:, 1] >= threshold).astype(int)
    y_test = data["test_labels"]
    mat = confusion_matrix(y_test, y)
    print(mat)
