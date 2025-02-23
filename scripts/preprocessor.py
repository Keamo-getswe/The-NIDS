import numpy as np
import pandas as pd
from logconfig import logger
import os

class Preprocessor:
    def __init__(self):
        pass

    def split_data(self, data):
        split_data = data.iloc[:, :-1]
        split_labels = data.iloc[:, -1]
        return split_data, split_labels
    
    def extract_dos_data(self, data):
        to_include = {'BENIGN', 'DoS Hulk', 'DoS slowloris', 'DoS GoldenEye', 'DoS Slowhttptest'}
        filtered_data = data[data['Label'].isin(to_include)]
        return filtered_data
    
    def enumerate_labels(self, labels):
        return labels.apply(lambda x: 0 if x == 'BENIGN' else 1)

    def handle_null_values(self, data):
        data = data.replace([np.inf, -np.inf], np.nan, inplace=False)
        data = data.dropna(inplace=False)
        return data
    
    def normalise_values(self, data, means, std_devs):
        means = means.to_numpy().reshape(1, -1)
        std_devs = std_devs.to_numpy().reshape(1, -1)
        res1 = data - means
        if res1.isna().values.any():
            res1 = res1.fillna(0)

        res2 = res1 / std_devs
        if res2.isna().values.any():
            res2 = res2.fillna(0)
        return res2

        
