#Dataset
DATASET_PATH = "CICIDS2017\\MachineLearningCVE"
NO_OF_FEATURES = 79
TEST_SIZE = 0.2
RANDOM_STATE_SEED = 42
TRAIN_TEST_DATA_PATH = "train_test_data.pkl"

#AE
TRAIN_INIT_SEED = 616
EPOCHS = 300
AE_FILE_PATH = "ae_model.pkl"

#TODO: Breaks at 15 going up. Investigate values in calculation that lead to this.
INPUT_DIMENSION = 11 #NO_OF_FEATURES - 1
HIDDEN_DIMENSION = 8 #int(0.5 * INPUT_DIMENSION)
BOTTLENECK_DIMENSION = 5 #int(0.5 * HIDDEN_DIMENSION)


