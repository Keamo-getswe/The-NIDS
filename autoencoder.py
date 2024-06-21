import numpy as np
import utility
import joblib
import os

class AutoEncoder:
    def __init__(self, in_dimension, hidden_dimension, learn_rate=0.1):
        self.__learning_rate = learn_rate
        np.random.seed(utility.TRAIN_INIT_SEED)
        self.__encoder_weights = np.random.randn(in_dimension, hidden_dimension)
        self.__decoder_weights = np.random.randn(hidden_dimension, in_dimension)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def derived_sigmoid(self, x):
        return np.exp(-x) / (1 + np.exp(-x))**2
    
    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return np.where(x > 0, 1, 0)

    def encode(self, data):
        z = np.dot(data, self.__encoder_weights)
        encoded_data = self.relu(z)
        return z, encoded_data

    def decode(self, data):
        z = np.dot(data, self.__decoder_weights)
        decoded_data = self.sigmoid(z)
        return z, decoded_data

    def calculate_loss(self, in_data, out_data):
        return np.mean((in_data - out_data) ** 2)
    
    def forward_pass(self, data):
        encoder_weight_sum, encoded_data = self.encode(data)
        decoder_weighted_sum, decoded_data = self.decode(encoded_data)
        return encoder_weight_sum, encoded_data, decoder_weighted_sum, decoded_data
        
    def backward_pass(self, in_data, e_weight_sum, e_data, d_weight_sum, d_data):
        err = in_data - d_data

        d_data_prime = -err * self.derived_sigmoid(d_weight_sum)
        d_weight_prime = np.dot(e_data.reshape(-1,1), d_data_prime.reshape(1, -1))

        e_data_prime = np.dot(d_data_prime, self.__decoder_weights.T) * self.relu_derivative(e_weight_sum)
        e_weight_prime = np.dot(in_data.reshape(-1,1), e_data_prime.reshape(1,-1))

        self.__encoder_weights -= self.__learning_rate * e_weight_prime
        self.__decoder_weights -= self.__learning_rate * d_weight_prime

    def train(self, data, epochs=utility.EPOCHS):
        #batch gradient decent
        for e in range(epochs):
            for _, r in data.iterrows():
                np_r = r.to_numpy()
                e_weight_sum, e_data, d_weight_sum, d_data = self.forward_pass(np_r)
                loss = self.calculate_loss(np_r, d_data)
                self.backward_pass(np_r, e_weight_sum, e_data, d_weight_sum, d_data)
            print(f'Epoch {e+1}/{epochs}, Loss: {loss}')

    def predict(self, data):
        _, _, _, decoded_data = self.forward_pass(data)
        return decoded_data
    
    def save_model(self):
        model_params = {
            'W1': self.__encoder_weights,
            'W2': self.__decoder_weights
        }

        file_path = utility.AE_FILE_PATH
        joblib.dump(model_params, file_path)

    def load_model(self):
        file_path = utility.AE_FILE_PATH
        model_params = joblib.load(file_path)
        self.__encoder_weights = model_params['W1']
        self.__decoder_weights = model_params['W2']