import joblib
from sklearn.ensemble import RandomForestClassifier

class RandomForest:
    def __init__(self):
        self.__classifier = RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)

    def train(self, data, labels):
        self.__classifier.fit(data, labels)

    def predict(self, data):
        return self.__classifier.predict(data)
    
    def save_model(self):
        joblib.dump(self.__classifier, "rf_model.pkl")

    def load_model(self):
        self.__classifier = joblib.load("rf_model.pkl")
