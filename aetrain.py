from autoencoder import AutoEncoder
from agent import Agent
import numpy as np
import joblib
import utility
import os

def get_benign_data(train_data, train_labels):
    indices = np.where(train_labels == 0)[0]
    selected_rows = train_data.iloc[indices]
    return selected_rows

def train_and_save_model():
    input_size = 5
    hidden_size = 3
    ae = AutoEncoder(input_size, hidden_size)
    agent = Agent("C:\\Users\\morob\\Documents\\Work\\Honours Project\\The-NIDS\\CICIDS2017\\MachineLearningCVE")
    train_data, train_labels, test_data, test_labels = agent.preprocess()

    #Because the autoencoder must be trained on benign data exclusively
    ae_train_data = get_benign_data(train_data, train_labels)
    ae_train_data = ae_train_data.iloc[:66]
    ae.train(ae_train_data)
    ae.save_model()
    data = {
        "train_data": train_data,
        "train_labels": train_labels,
        "test_data": test_data,
        "test_labels": test_labels
    }
    joblib.dump(data, utility.TRAIN_TEST_DATA_PATH)

if __name__ == "__main__":
    train_and_save_model()