import numpy as np
import pandas as pd

class Preprocessor:
    def __init__(self):
        pass

    def extract_features(self, data):
        #features = [' Destination Port', ' Flow Duration', ' Total Fwd Packets', ' Total Backward Packets', ' Fwd Packet Length Mean', 'Flow Bytes/s']
        features = [' Destination Port', ' Flow Duration', ' Total Fwd Packets', ' Total Backward Packets', 'Flow Bytes/s']
        data = data[features]
        print("Preprocessor: Successful feature extraction.")
        return data

    def handle_null_values(self, data):
        data = data.dropna(inplace=False)
        data = data.replace([np.inf, -np.inf], np.nan, inplace=False)

        print("Preprocessor: Successful null value handling.")
        return data
    
    def normalise_values(self, data):
        means = data.mean(axis=0)
        std_devs = data.std(axis=0)
        
        # Standardize the data
        print("Preprocessor: Successful standardisation.")
        return (data - means) / std_devs

    def process_data(self, data):
        processed_data = self.handle_null_values(data)
        processed_data = self.extract_features(processed_data)
        processed_data = self.normalise_values(processed_data)
        return processed_data