from PySide6 import QtCore
from PySide6.QtCore import QObject
from filereader import FileReader
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from preprocessor import Preprocessor
import pandas as pd
import joblib
import utility
from logconfig import logger
import sys

class Agent(QObject):
    new_data = QtCore.Signal(list)

    def __init__(self):
        super().__init__()
        self.__preprocessor = Preprocessor()

    def set_data_from_files(self, path="C:\\Users\\morob\\Documents\\Work\\Honours Project\\The-NIDS\\CICIDS2017\\MachineLearningCVE"):
        fileReader = FileReader(path)
        return fileReader.read_training_files()
    
    def save_normalization_data(self, means, std_devs):
        normal_data = {
            "means": means,
            "std_devs": std_devs,
        }
        joblib.dump(normal_data, utility.NORMALIZATION_DATA)

    def load_normalization_data(self):
        normal_data = joblib.load(utility.NORMALIZATION_DATA)
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
        desired_majority = int(majority_count * 0.8)

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

        #Enumerate labels
        processed_train_labels = self.__preprocessor.enumerate_labels(processed_train_labels)
        processed_test_labels = self.__preprocessor.enumerate_labels(processed_test_labels)

        return processed_train_data.iloc[:, :utility.INPUT_DIMENSION], processed_train_labels.iloc[:], processed_test_data.iloc[:, :utility.INPUT_DIMENSION], processed_test_labels
    
    def pipelineb_training_preprocess(self):
        data = self.set_data_from_files()

        if data is None:
            logger.critical("Training data is empty.")
            return None, None, None, None
        else:
            logger.info("Training data loaded successfully from files.")

        processed_data = self.__preprocessor.handle_null_values(data)
        processed_data = self.__preprocessor.extract_dos_data(processed_data)

    def prepare_production_preprocess(self):
        self.means, self.std_devs = self.load_normalization_data()
    
    def production_preprocess(self, data):
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
        