from agent import Agent
import numpy as np
from sklearn.decomposition import PCA
from sklearn.metrics import f1_score, precision_score, recall_score, confusion_matrix
from lstmautoencoder import LSTMAutoencoder
import utility
import joblib
import sys

if __name__ == "__main__":
    agent = Agent()
    train_sequences, y_train, test_sequences, y_test = agent.pipelineb_training_preprocess()
    lstm_ae = LSTMAutoencoder(training=False)
    # lstm_ae.train(train_sequences)
    # sys.exit(0)
    pred, _, anomalies = lstm_ae.predict(test_sequences)
    precision = precision_score(y_test, anomalies)
    recall = recall_score(y_test, anomalies)
    f1 = f1_score(y_test, anomalies)
    tn, fp, fn, tp = confusion_matrix(y_test, anomalies).ravel()
    print("Train metrics:\n")
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1_Score:", f1)
    print(f'True Positives: {tp}')
    print(f'True Negatives: {tn}')
    print(f'False Positives: {fp}')
    print(f'False Negatives: {fn}')