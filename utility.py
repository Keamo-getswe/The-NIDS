from PySide6 import QtCore
from PySide6.QtCore import QDate
import re 

#Dataset
DATASET_PATH = "CICIDS2017\\MachineLearningCVE" #Change to training dataset path
#Add production dataset path
NO_OF_FEATURES = 79
TEST_SIZE = 0.2
RANDOM_STATE_SEED = 42
P1_TRAIN_TEST_DATA_PATH = "train_test_data.pkl"
P2_TRAIN_TEST_DATA_PATH = "p2_train_test_data.pkl"
P1_NORMALIZATION_DATA = "p1_normal_data.pkl"

# This is actually the scaler since the MinMaxScaler was used here
P2_NORMALIZATION_DATA = "p2_normal_data.pkl"
IMPUTER = "imputer.pkl"

#AE
TRAIN_INIT_SEED = 560
EPOCHS = 50
AE_FILE_PATH = "ae_model.pkl"
AE_TEMP_PATH = "ae_model2.pkl"

#RF
RF_FILE_PATH = "rf_model.pkl"

#PCA
PCA_FILE_PATH = "pca_model.pkl"

#LSTM AE
LSTM_SEQUENCE_LENGTH = 20
LSTM_NUM_FEATURES = 12 
LSTM_AE_MODEL_FILE_PATH = "lstm_autoencoder.keras"
LSTM_AE_SUPPORT_FILE_PATH = "lstm_support.pkl" # Scope for predicting using regression data

#TODO: Breaks at 15 going up. Investigate values in calculation that lead to this.
INPUT_DIMENSION = NO_OF_FEATURES - 1
HIDDEN_DIMENSION = int(0.5 * INPUT_DIMENSION)
BOTTLENECK_DIMENSION = int(0.5 * HIDDEN_DIMENSION) + 3

# Network Information
with open("config.txt", "r") as file:
    txt = file.read()

SOURCE_IP = re.findall(r"(([0-9]{1,3}[.]){3}([0-9]{1,3}))", txt)[0][0]
DESTINATION_IP = re.findall(r"(([0-9]{1,3}[.]){3}([0-9]{1,3}))", txt)[1][0]
PORT = 17000