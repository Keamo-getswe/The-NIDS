import numpy as np
import pandas as pd
import utility
import os

class Preprocessor:
    def __init__(self):
        pass

    def split_data(self, data):
        split_data = data.iloc[:, :-1]
        split_labels = data.iloc[:, -1]
        return split_data, split_labels
    
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
