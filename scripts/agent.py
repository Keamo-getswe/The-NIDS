from PySide6 import QtCore
from PySide6.QtCore import QObject
from filereader import FileReader
from lstmfilereader import LstmFileReader 
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from preprocessor import Preprocessor
from lstmpreprocessor import LstmPreprocessor
import pandas as pd
import joblib
import utility
from logconfig import logger
import sys
import numpy as np

class Agent(QObject):
    new_data = QtCore.Signal(list)

    def __init__(self, training=True):
        super().__init__()
        self.__preprocessor = Preprocessor()
        self.__lstmpreprocessor = LstmPreprocessor(training)
        self.time_series_buffer = pd.DataFrame()
        self.lstm_seq_len = utility.LSTM_SEQUENCE_LENGTH
        self.pca = None
        if training:    
            self.pca = PCA(n_components=12)
        else:
            self.pca = joblib.load(utility.PCA_FILE_PATH)
    # Redacted path
    def set_data_from_files(self, path=utility.P1_TRAINING_DATASET_PATH):
        file_reader = FileReader(path)
        return file_reader.read_training_files()

    # Redacted path
    def set_temporal_data_from_files(self, path=utility.P2_TRAINING_DATASET_PATH):
        reader = LstmFileReader(path)
        train_data = reader.read_training_files()
        test_data = reader.read_test_file()
        return train_data, test_data
    
    def save_normalization_data(self, means, std_devs):
        normal_data = {
            "means": means,
            "std_devs": std_devs,
        }
        joblib.dump(normal_data, utility.P1_NORMALIZATION_DATA)

    def load_normalization_data(self):
        normal_data = joblib.load(utility.P1_NORMALIZATION_DATA)
        means, std_devs = normal_data["means"], normal_data["std_devs"]
        return means, std_devs

    def pipelinea_training_preprocess(self):
        data = self.set_data_from_files()

        if data is None:
            logger.critical("Training data is empty.")
            return None, None, None, None
        else:
            logger.info("Training data loaded successfully from files.")

        processed_data = self.__preprocessor.handle_null_values(data)
        processed_data = self.__preprocessor.extract_dos_data(processed_data)

        #Train/test split data
        processed_train_data, processed_test_data = train_test_split(processed_data, test_size=utility.TEST_SIZE,
                                                     random_state=utility.RANDOM_STATE_SEED)
        
        processed_train_data, processed_train_labels = self.__preprocessor.split_data(processed_train_data)
        processed_test_data, processed_test_labels = self.__preprocessor.split_data(processed_test_data)
        
        majority_count = processed_train_labels.value_counts().max()
        desired_majority = int(majority_count * 0.6)

        #Decrease majority class (decided for convenience of time of experimental computations)
        undersampler = RandomUnderSampler(
            sampling_strategy={
                "BENIGN": desired_majority
        })
        processed_train_data, processed_train_labels = undersampler.fit_resample(processed_train_data, processed_train_labels)
        majority_count = processed_train_labels.value_counts().max()
        target_count = int(0.4 * majority_count)

        #Augment data to account for class imbalance (and possibly regularize)
        smote_oversampler = SMOTE(
            random_state=utility.RANDOM_STATE_SEED,
            sampling_strategy={
                'DoS Hulk': target_count,
                'DoS slowloris': target_count,
                'DoS GoldenEye': target_count,
                'DoS Slowhttptest': target_count
        })
        processed_train_data, processed_train_labels = smote_oversampler.fit_resample(processed_train_data, processed_train_labels)
        majority_count = processed_train_labels.value_counts().max()

        #Normalise data
        means = processed_train_data.mean(axis=0)
        std_devs = processed_train_data.std(axis=0)
        self.save_normalization_data(means, std_devs) #For use on test and production data
        processed_train_data = self.__preprocessor.normalise_values(processed_train_data, means, std_devs)
        processed_test_data = self.__preprocessor.normalise_values(processed_test_data, means, std_devs)

        #Enumerate labels
        processed_train_labels = self.__preprocessor.enumerate_labels(processed_train_labels)
        processed_test_labels = self.__preprocessor.enumerate_labels(processed_test_labels)

        return processed_train_data.iloc[:, :utility.INPUT_DIMENSION], processed_train_labels.iloc[:], processed_test_data.iloc[:, :utility.INPUT_DIMENSION], processed_test_labels
    
    def pipelineb_training_preprocess(self):
        train_data, test_data = self.set_temporal_data_from_files()

        if train_data is None:
            logger.critical("Training data is empty.")
            return None, None, None, None
        else:
            logger.info("Training data loaded successfully from files.")
        
        if test_data is None:
            logger.critical("Test data is empty.")
            return None, None, None, None
        else:
            logger.info("Test data loaded successfully from files.")

        train_data = self.__lstmpreprocessor.enumerate_labels(train_data)
        test_data = self.__lstmpreprocessor.enumerate_labels(test_data)

        train_data =  self.__lstmpreprocessor.filter_benign_labels(train_data)

        train_data, train_labels = self.__lstmpreprocessor.split_data(train_data)
        test_data, test_labels = self.__lstmpreprocessor.split_data(test_data)
        processed_train_data = self.__lstmpreprocessor.handle_null_values(train_data)
        processed_test_data = self.__lstmpreprocessor.handle_null_values(test_data)
        
        processed_train_data = pd.DataFrame(self.__lstmpreprocessor.normalise_train_values(processed_train_data))
        processed_train_data = pd.DataFrame(self.__lstmpreprocessor.handle_null_values(processed_train_data))
        processed_test_data = pd.DataFrame(self.__lstmpreprocessor.normalise_test_values(processed_test_data))
        processed_test_data = pd.DataFrame(self.__lstmpreprocessor.handle_null_values(processed_test_data))

        processed_train_data = pd.DataFrame(self.pca.fit_transform(processed_train_data))
        processed_test_data = pd.DataFrame(self.pca.fit_transform(processed_test_data))
        joblib.dump(self.pca, utility.PCA_FILE_PATH)

        time_steps = 20
        train_sequences = self.create_sequences(processed_train_data, time_steps)
        test_sequences = self.create_sequences(processed_test_data, time_steps)

        return train_sequences, train_labels.iloc[:-20], test_sequences, test_labels.iloc[:-20]

    def create_sequences(self, data, time_steps): # Split data into sequences
        sequences = []
        for i in range(len(data) - time_steps):
            seq = data[i:i + time_steps]
            sequences.append(seq)
        return np.array(sequences)

    def prepare_p1_production_preprocess(self):
        self.means, self.std_devs = self.load_normalization_data()
    
    def p1_production_preprocess(self, data):
        data = [float(x) for x in data.split(",")[:-1]]
        if not len(data) == utility.INPUT_DIMENSION:
            logger.error("Agent detects an incorrect number of features during preprocessing. Dropping data point.")
            return None
        self.new_data.emit(data)
        df = pd.DataFrame(data)
        df = df.T
        df = self.__preprocessor.handle_null_values(df)
        df = self.__preprocessor.normalise_values(df, self.means, self.std_devs)
        return df
    
    def p2_production_preprocess(self, data):
        data = [float(x) for x in data.split(",")[:-1]]
        if not len(data) == utility.INPUT_DIMENSION:
            logger.error("Agent detects an incorrect number of features during preprocessing. Dropping data point.")
            return None
        self.new_data.emit(data)
        data = pd.DataFrame(data).T
        self.update_buffer(data)
        
        if len(self.time_series_buffer) == self.lstm_seq_len:
            self.time_series_buffer = self.__lstmpreprocessor.handle_null_values(self.time_series_buffer)
            self.time_series_buffer = self.__lstmpreprocessor.normalise_test_values(self.time_series_buffer)
            self.time_series_buffer = self.pca.transform(self.time_series_buffer)
            input_sequence = np.array([self.time_series_buffer])
            return input_sequence
        
        return None

    def update_buffer(self, data):
        if not isinstance(self.time_series_buffer, pd.DataFrame):
            self.time_series_buffer = pd.DataFrame(self.time_series_buffer)

        self.time_series_buffer = pd.concat([self.time_series_buffer, data], ignore_index=True)
        if len(self.time_series_buffer) > self.lstm_seq_len:
            self.time_series_buffer = self.time_series_buffer.iloc[1:]