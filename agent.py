from filereader import FileReader
from sklearn.model_selection import train_test_split
from preprocessor import Preprocessor
import pandas as pd
import joblib
import utility
import sys

class Agent():
    def __init__(self):
        self.__preprocessor = Preprocessor()

    def set_data_from_files(self, path="C:\\Users\\morob\\Documents\\Work\\Honours Project\\The-NIDS\\CICIDS2017\\MachineLearningCVE"):
        fileReader = FileReader(path)
        return fileReader.read_files()
    
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

    def training_preprocess(self):
        data = self.set_data_from_files()

        processed_data = self.__preprocessor.handle_null_values(data)
        #processed_data = self.__preprocessor.extract_features(processed_data)

        #Train/test split data
        processed_train_data, processed_test_data = train_test_split(processed_data, test_size=utility.TEST_SIZE,
                                                     random_state=utility.RANDOM_STATE_SEED)
        
        processed_train_data, processed_train_labels = self.__preprocessor.split_data(processed_train_data)
        processed_test_data, processed_test_labels = self.__preprocessor.split_data(processed_test_data)
        
        #Normalise data
        means = processed_train_data.mean(axis=0)
        std_devs = processed_train_data.std(axis=0)
        self.save_normalization_data(means, std_devs) #For use on test and production data
        processed_train_data = self.__preprocessor.normalise_values(processed_train_data, means, std_devs)

        #Enumerate labels
        processed_train_labels = self.__preprocessor.enumerate_labels(processed_train_labels)
        processed_test_labels = self.__preprocessor.enumerate_labels(processed_test_labels)

        return processed_train_data.iloc[:, :utility.INPUT_DIMENSION], processed_train_labels, processed_test_data.iloc[:, :utility.INPUT_DIMENSION], processed_test_labels
    
    def prepare_production_preprocess(self):
        self.means, self.std_devs = self.load_normalization_data()
    
    def production_preprocess(self, data):
        data = [float(x) for x in data.split(",")[:-1]]
        df = pd.DataFrame(data)
        df = df.T
        df = self.__preprocessor.handle_null_values(df)
        df = self.__preprocessor.normalise_values(df, self.means, self.std_devs)
        return df.iloc[:,:utility.INPUT_DIMENSION]
        