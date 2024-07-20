import numpy as np
import utility
import joblib
import os
import matplotlib.pyplot as plt

np.seterr(over='raise', under='raise')

class AutoEncoder:
    def __init__(self, in_dimension, h1_dimension, learn_rate=0.01):
        self.__learning_rate = learn_rate
        #np.random.seed(utility.TRAIN_INIT_SEED)
        self.__encoder_w1 = self.xavier_init((in_dimension, h1_dimension))
        self.__encoder_b1 = np.random.randn(1, h1_dimension)
        self.__encoder_w2 = self.xavier_init((h1_dimension, utility.BOTTLENECK_DIMENSION))
        self.__encoder_b2 = np.random.randn(1, utility.BOTTLENECK_DIMENSION)

        self.__decoder_w1 = self.xavier_init((utility.BOTTLENECK_DIMENSION, h1_dimension))
        self.__decoder_b1 = np.random.randn(1, h1_dimension)
        self.__decoder_w2 = self.xavier_init((h1_dimension, in_dimension))
        self.__decoder_b2 = np.random.randn(1, in_dimension)

    def xavier_init(self, size):
        return np.random.randn(*size) * np.sqrt(1.0 / size[0])
    
    def sigmoid(self, x):
        try:
            safe_x = np.clip(x, -700, 700)
            z = 1 / (1 + np.exp(-safe_x))
        except FloatingPointError as fpe:
            print("Sigmoid error", x)
            os._exit(0)

        return z

    def derived_sigmoid(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))
    
    def relu(self, x):
        return np.maximum(0, x)

    def relu_derivative(self, x):
        return np.where(x > 0, 1, 0)

    def encode(self, data):
        self.h1_input = np.dot(data, self.__encoder_w1) + self.__encoder_b1
        self.h1_data = self.relu(self.h1_input)
        self.latent_input = np.dot(self.h1_data, self.__encoder_w2) + self.__encoder_b2
        self.encoded_data = self.relu(self.latent_input)

    def get_encoded_data(self):
        return self.encoded_data
        
    def decode(self, data):
        self.h2_input = np.dot(data, self.__decoder_w1) + self.__decoder_b1
        self.h2_data = self.relu(self.h2_input)
        self.outlayer_input = np.dot(self.h2_data, self.__decoder_w2) + self.__decoder_b2
        self.decoded_data = self.sigmoid(self.outlayer_input)

    def get_decoded_data(self):
        return self.decoded_data

    def calculate_loss(self, in_data, out_data):
        return np.mean((in_data - out_data) ** 2)
    
    def forward_pass(self, data):
        self.encode(data)
        self.decode(self.get_encoded_data())
        
    def backward_pass(self, in_data):
        err = in_data - self.decoded_data

        outlayer_error = -err * self.derived_sigmoid(self.outlayer_input)
        d_w2_prime = np.dot(self.h2_data.T, outlayer_error)
        d_bias2_prime = np.sum(outlayer_error, axis=0)

        h2_error = np.dot(outlayer_error, self.__decoder_w2.T) * self.relu_derivative(self.h2_input)
        d_w1_prime = np.dot(self.encoded_data.T, h2_error)
        d_bias1_prime = np.sum(h2_error, axis=0)

        latent_error = np.dot(h2_error, self.__decoder_w1.T) * self.relu_derivative(self.latent_input)
        e_w2_prime = np.dot(self.h1_data.T, latent_error)
        e_bias2_prime = np.sum(latent_error, axis=0)

        h1_error = np.dot(latent_error, self.__encoder_w2.T) * self.relu_derivative(self.h1_input)
        e_w1_prime = np.dot(in_data.T, h1_error)
        e_bias1_prime = np.sum(h1_error, axis=0)

        #Update weights and biases
        self.__encoder_w1 -= self.__learning_rate * e_w1_prime
        self.__encoder_b1 -= self.__learning_rate * e_bias1_prime
        self.__encoder_w2 -= self.__learning_rate * e_w2_prime
        self.__encoder_b2 -= self.__learning_rate * e_bias2_prime

        self.__decoder_w1 -= self.__learning_rate * d_w1_prime
        self.__decoder_b1 -= self.__learning_rate * d_bias1_prime
        self.__decoder_w2 -= self.__learning_rate * d_w2_prime
        self.__decoder_b2 -= self.__learning_rate * d_bias2_prime.to_numpy()

    def train(self, data, epochs=utility.EPOCHS):
        N = data.shape[0]
        batch_size = 3
        losses = []
        #batch gradient decent
        for e in range(epochs):
            # Shuffle data
            indices = np.arange(N)
            np.random.shuffle(indices)
            data = data.iloc[indices]
        
            for i in range(0, N, batch_size):
                batch_data = data[i:i + batch_size]
                self.forward_pass(batch_data)
                loss = self.calculate_loss(batch_data, self.decoded_data)
                losses += [loss]
                self.backward_pass(batch_data)
            print(f'Epoch {e+1}/{epochs}, Loss: {loss}')
            
        x = np.linspace(-100, 100, len(losses))
        y = np.array(losses)
        plt.plot(x, y)
        plt.show()

    def predict(self, data):
        _, _, _, decoded_data = self.forward_pass(data)
        return decoded_data
    
    def save_model(self):
        model_params = {
            'E_W1': self.__encoder_w1,
            'D_W1': self.__decoder_w1,
            'E_b1': self.__encoder_b1,
            'D_b1': self.__decoder_b1
        }

        file_path = utility.AE_FILE_PATH
        joblib.dump(model_params, file_path)

    def load_model(self):
        file_path = utility.AE_FILE_PATH
        model_params = joblib.load(file_path)
        self.__encoder_w1 = model_params['E_W1']
        self.__decoder_w1 = model_params['D_W1']
        self.__encoder_b1 = model_params['E_b1']
        self.__decoder_b1 = model_params['D_b1']