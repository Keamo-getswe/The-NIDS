import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import utility
import os

class Preprocessor:
    def __init__(self):
        pass

    def split_train_data(self, train_data):
        split_train_data = train_data.iloc[:, :-1]
        split_train_labels = train_data.iloc[:, -1]
        return split_train_data, split_train_labels

    def split_test_data(self, test_data):
        split_test_data = test_data.iloc[:, :-1]
        split_test_labels = test_data.iloc[:, -1]
        return split_test_data, split_test_labels
    
    def enumerate_labels(self, labels):
        return labels.apply(lambda x: 0 if x == 'BENIGN' else 1)

    def extract_features(self, data):
        features = [' Destination Port', ' Flow Duration', ' Total Fwd Packets', ' Total Backward Packets', 'Flow Bytes/s', ' Label']
        data = data[features]
        return data

    def handle_null_values(self, data):
        data = data.dropna(inplace=False)
        data = data.replace([np.inf, -np.inf], np.nan, inplace=False)
        return data
    
    def normalise_values(self, data):
        means = data.mean(axis=0)
        std_devs = data.std(axis=0)
        return (data - means) / std_devs

    def process_data(self, data):
        processed_data = self.handle_null_values(data)
        #processed_data = self.extract_features(processed_data)

        #Train/test split data
        processed_train_data, processed_test_data = train_test_split(processed_data, test_size=utility.TEST_SIZE,
                                                     random_state=utility.RANDOM_STATE_SEED)
        
        processed_train_data, processed_train_labels = self.split_train_data(processed_train_data)
        processed_test_data, processed_test_labels = self.split_test_data(processed_test_data)
        
        #Normalise data
        processed_train_data = self.normalise_values(processed_train_data)
        processed_test_data = self.normalise_values(processed_test_data)

        #Enumerate labels
        processed_train_labels = self.enumerate_labels(processed_train_labels)
        processed_test_labels = self.enumerate_labels(processed_test_labels)

        return processed_train_data.iloc[:, :utility.INPUT_DIMENSION], processed_train_labels, processed_test_data.iloc[:, :utility.INPUT_DIMENSION], processed_test_labels