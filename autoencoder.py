import numpy as np
from utility import SEED_VALUE
from agent import Agent

class AutoEncoder:
    def __init__(self, in_dimension, hidden_dimension, learn_rate=0.00001):
        self.__input_dim = in_dimension #input and output layer size
        self.__hidden_dim = hidden_dimension #bottleneck layer size
        self.__learning_rate = learn_rate

        np.random.seed(616)
        self.__encoder_weights = np.random.randn(self.__input_dim, self.__hidden_dim)
        self.__decoder_weights = np.random.randn(self.__hidden_dim, self.__input_dim)
        print("Autoencoder: Constructed")

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def derived_sigmoid(self, x):
        return x * (1 - x)
    
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

        d_data_prime = err * self.derived_sigmoid(d_weight_sum)
        d_weight_prime = np.dot(e_data.T, d_data_prime)

        e_data_prime = np.dot(d_data_prime, self.__decoder_weights.T) * self.relu_derivative(e_weight_sum)
        e_weight_prime = np.dot(in_data.T, e_data_prime)

        self.__encoder_weights -= self.__learning_rate * e_weight_prime
        self.__decoder_weights -= self.__learning_rate * d_weight_prime

    def train(self, data, epochs=100):
        #batch gradient decent
        for e in range(epochs):
            e_weight_sum, e_data, d_weight_sum, d_data = self.forward_pass(data)

            loss = self.calculate_loss(data, d_data)
            print(f'Epoch {e+1}/{epochs}, Loss: {loss}')

            self.backward_pass(data, e_weight_sum, e_data, d_weight_sum, d_data)

    def predict(self, data):
        z1 = np.dot(data, self.__encoder_weights)
        encoded_data = self.relu(z1)
        z2 = np.dot(encoded_data, self.__decoder_weights)
        decoded_data = self.sigmoid(z2)
        return decoded_data


agent = Agent("C:\\Users\\morob\\Documents\\Work\\Honours Project\\The NIDS\\CICIDS2017\\MachineLearningCVE")
data = agent.preprocess()
ae = AutoEncoder(5, 3)
ae.train(data)