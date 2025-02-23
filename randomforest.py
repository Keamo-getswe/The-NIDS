import joblib
from sklearn.ensemble import RandomForestClassifier
import utility
import numpy as np

class RandomForest:
    def __init__(self):
        self.__classifier = RandomForestClassifier(n_estimators=500, criterion='entropy', max_features=79, random_state=0, class_weight='balanced_subsample')

    def train(self, data, labels):
        self.__classifier.fit(data, labels)

    def predict(self, data):
        return self.__classifier.predict_proba(data)
    
    def save_model(self):
        joblib.dump(self.__classifier, utility.RF_FILE_PATH)

    def load_model(self):
        self.__classifier = joblib.load(utility.RF_FILE_PATH)