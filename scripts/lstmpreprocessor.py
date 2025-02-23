from preprocessor import Preprocessor
# from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import joblib
import utility
import pandas as pd

pd.set_option('future.no_silent_downcasting', True)

class LstmPreprocessor(Preprocessor):
    def __init__(self, training=True):
        super().__init__()
        self.training = training
        self.has_fitted_imputer = False
        self.has_fitted_scaler = False
        self.imputer = None
        self.scaler = None
        if self.training:
            # self.imputer = KNNImputer(n_neighbors=2, weights="distance")
            self.scaler = MinMaxScaler(feature_range=(0, 1))
        else:
            self.imputer = joblib.load(utility.IMPUTER)
            self.has_fitted_imputer = True
            self.scaler = joblib.load(utility.P2_NORMALIZATION_DATA)
            self.has_fitted_scaler = True

    # def handle_null_values(self, data):
    #     data.replace([np.inf, -np.inf], np.nan, inplace=True)
    #     data = data.to_numpy()
    #     if not self.has_fitted_imputer:
    #         self.imputer.fit(data)
    #         self.has_fitted_imputer = True
    #     data_imputed = self.imputer.transform(data)
    #     return data_imputed

    def handle_null_values(self, data):
        window = 3
        data.replace([np.inf, -np.inf], np.nan, inplace=True)
        
        filled_data = data.ffill()
        rolling_mean = filled_data.rolling(window=window, min_periods=1).mean()
        filled_data = filled_data.fillna(rolling_mean)
        filled_data = filled_data.fillna(filled_data.mean())
        
        return filled_data
    
    def extract_dos_data(self, data):
        pass

    def normalise_values(self, data, means, std_devs):
        pass

    def enumerate_labels(self, data):
        data['Label'] = data['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1)
        return data
    
    def filter_benign_labels(self, data):
        data = data[data['Label'] == 0]
        return data

    def normalise_train_values(self, data):
        if not self.has_fitted_scaler:
            self.scaler.fit(data)
            self.has_fitted_scaler = True
        data_scaled = self.scaler.transform(data)
        joblib.dump(self.scaler, utility.P2_NORMALIZATION_DATA)
        return data_scaled

    def normalise_test_values(self, data): #Also handles production values
        data_scaled = self.scaler.transform(data)
        data_scaled = self.handle_null_values(data)
        return data_scaled
