from randomforest import RandomForest
from autoencoder import AutoEncoder
from agent import Agent
import joblib
import utility

def train_and_save_model():
    rf = RandomForest()
    ae = AutoEncoder(5, 3)
    ae.load_model()
    data = joblib.load(utility.TRAIN_TEST_DATA_PATH)
    train_data = data["train_data"]
    _, reduced_features = ae.encode(train_data)
    train_labels = data["train_labels"]
    rf.train(reduced_features, train_labels)
    rf.save_model()

if __name__ == "__main__":
    train_and_save_model()