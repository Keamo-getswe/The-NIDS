from randomforest import RandomForest
from autoencoder import AutoEncoder
import cupy as cp
import joblib
import utility
import os

def train_and_save_model():
    rf = RandomForest()
    input_size = utility.INPUT_DIMENSION
    hidden_size = [utility.HIDDEN_DIMENSION, utility.BOTTLENECK_DIMENSION]
    ae = AutoEncoder(input_size, hidden_size)
    ae.load_model()
    data = joblib.load(utility.TRAIN_TEST_DATA_PATH)
    train_data = data["train_data"]
    ae.encode(cp.array(train_data.to_numpy()))
    reduced_features = ae.get_encoded_data()
    train_labels = data["train_labels"]
    reduced_features = cp.asnumpy(reduced_features)
    rf.train(reduced_features, train_labels)
    rf.save_model()

if __name__ == "__main__":
    train_and_save_model()