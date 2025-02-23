import re 

#Datasets
P1_TRAINING_DATASET_PATH = "..\\data\\raw\\CICIDS2017\\MachineLearningCVE" #Change to training dataset path
P2_TRAINING_DATASET_PATH = "..\\data\\raw\\CSE-CIC-IDS2018"
#Add production dataset path
NO_OF_FEATURES = 79
TEST_SIZE = 0.2
RANDOM_STATE_SEED = 42
P1_TRAIN_TEST_DATA_PATH = "..\\data\\preprocessed\\train_test_data.pkl"
P2_TRAIN_TEST_DATA_PATH = "..\\data\\preprocessed\\p2_train_test_data.pkl"
P1_NORMALIZATION_DATA = "..\\data\\cached\\p1_normal_data.pkl"

# This is actually the scaler since the MinMaxScaler was used here
P2_NORMALIZATION_DATA = "..\\data\\cached\\p2_normal_data.pkl"
IMPUTER = "..\\data\\cached\\imputer.pkl"

#AE
TRAIN_INIT_SEED = 560
EPOCHS = 50
AE_FILE_PATH = "..\\models\\trained\\pipelineA\\ae_model.pkl"
INPUT_DIMENSION = NO_OF_FEATURES - 1
HIDDEN_DIMENSION = int(0.5 * INPUT_DIMENSION)
BOTTLENECK_DIMENSION = int(0.5 * HIDDEN_DIMENSION) + 3

#RF
RF_FILE_PATH = "..\\models\\trained\\pipelineA\\rf_model.pkl"

#PCA
PCA_FILE_PATH = "..\\models\\trained\\pipelineB\\pca_model.pkl"

#LSTM AE
LSTM_SEQUENCE_LENGTH = 20
LSTM_NUM_FEATURES = 12 
LSTM_AE_MODEL_FILE_PATH = "..\\models\\trained\\pipelineB\\lstm_autoencoder.keras"
LSTM_AE_SUPPORT_FILE_PATH = "..\\models\\trained\\pipelineB\\lstm_support.pkl" # Scope for predicting using regression data

# Network Information
with open("..\\configuration\\config.txt", "r") as file:
    txt = file.read()

SOURCE_IP = re.findall(r"(([0-9]{1,3}[.]){3}([0-9]{1,3}))", txt)[0][0]
DESTINATION_IP = re.findall(r"(([0-9]{1,3}[.]){3}([0-9]{1,3}))", txt)[1][0]
PORT = 17000

ICON_PATH = "..\\resources\\images\\"

