from randomforest import RandomForest
from autoencoder import AutoEncoder
import joblib
import utility
import os

def train_and_save_model():
    rf = RandomForest()
    input_size = utility.INPUT_DIMENSION
    hidden_size = utility.HIDDEN_DIMENSION
    ae = AutoEncoder(input_size, hidden_size)
    ae.load_model()
    data = joblib.load(utility.TRAIN_TEST_DATA_PATH)
    train_data = data["train_data"]
    ae.encode(train_data)
    reduced_features = ae.get_encoded_data()
    train_labels = data["train_labels"]
    rf.train(reduced_features, train_labels)
    rf.save_model()

if __name__ == "__main__":
    train_and_save_model()