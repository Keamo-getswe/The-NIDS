import numpy as np
import cupy as cp
import utility
import joblib
import os
import math

np.seterr(over='raise', under='raise')

class BatchNormalization:
    def __init__(self, input_size, epsilon=1e-8):
        self.epsilon = epsilon
        self.gamma = cp.ones((1, input_size))
        self.beta = cp.zeros((1, input_size))
        self.batch_mean = None
        self.batch_var = None
        self.running_mean = cp.zeros((1, input_size))
        self.running_var = cp.ones((1, input_size))
        self.momentum = 0.9
        
    def forward(self, X, training=True):
        if training:
            self.batch_mean = cp.mean(X, axis=0)
            self.batch_var = cp.var(X, axis=0)
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * self.batch_mean
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * self.batch_var
            self.X_norm = (X - self.batch_mean) / cp.sqrt(self.batch_var + self.epsilon)
        else:
            self.X_norm = (X - self.running_mean) / cp.sqrt(self.running_var + self.epsilon)

        out = self.gamma * self.X_norm + self.beta
        return out
    
    def backward(self, X, dout):
        N = dout.shape[0]

        dX_norm = cp.array(dout * self.gamma)
        dvar = cp.array(cp.sum(dX_norm * (self.X_norm * (-0.5) * (self.batch_var + self.epsilon)**(-3/2)), axis=0))
        dmean = cp.array(cp.sum(dX_norm * (-1.0 / cp.sqrt(self.batch_var + self.epsilon)), axis=0) + dvar * cp.mean(-2.0 * self.X_norm, axis=0))
        dX_term1 = -dX_norm / cp.array(cp.sqrt(self.batch_var + self.epsilon))
        dX_term2 = 2.0 * dvar.reshape(1, -1) * (self.X_norm * cp.sqrt(self.batch_var + self.epsilon)) / N
        dX_term3 = (dmean / N).reshape(1, -1)
        dX = dX_term1 + dX_term2 + dX_term3
        dgamma = cp.sum(dout * self.X_norm, axis=0)
        dbeta = cp.sum(dout, axis=0)

        return dX, dgamma, dbeta

class AutoEncoder:
    def __init__(self, in_dimension, hidden_dimensions, learn_rate=0.0001, reg_lambda=1e-7, dropout_rate=0.2):
        self.learning_rate = learn_rate
        self.hidden_sizes = hidden_dimensions
        self.num_layers = len(hidden_dimensions)
        cp.random.seed(utility.TRAIN_INIT_SEED)
        self.reg_lambda = reg_lambda  #regularization strength
        # self.dropout_rate = dropout_rate  #dropout probability
        # self.dropout_masks = []

        self.weights = []
        self.biases = []
        # self.batch_norms = []

        prev_size = in_dimension
        #init encoder weights and biases
        for hidden_size in hidden_dimensions:
            self.weights.append(self.xavier_init((prev_size, hidden_size)))
            self.biases.append(cp.random.randn(1, hidden_size))
            # self.batch_norms.append(BatchNormalization(hidden_size))
            prev_size = hidden_size

        #init decoder weights and biases
        for hidden_size in reversed(hidden_dimensions):
            if prev_size == hidden_size:
                continue
            self.weights.append(self.xavier_init((prev_size, hidden_size)))
            self.biases.append(cp.random.randn(1, hidden_size))
            # self.batch_norms.append(BatchNormalization(hidden_size))
            prev_size = hidden_size

        self.weights.append(self.xavier_init((prev_size, in_dimension)))
        self.biases.append(cp.random.randn(1, in_dimension))
        # self.batch_norms.append(BatchNormalization(in_dimension))

    def xavier_init(self, size):
        return cp.random.randn(*size) * cp.sqrt(1.0 / size[0])
    
    def sigmoid(self, x):
        try:
            safe_x = cp.clip(x, -700, 700)
            z = 1 / (1 + cp.exp(-safe_x))
        except FloatingPointError as fpe:
            print("Sigmoid error", x)
            os._exit(0)

        return z

    def sigmoid_derivative(self, x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))
    
    def relu(self, x):
        return cp.maximum(0, x)

    def relu_derivative(self, x):
        return cp.where(x > 0, 1, 0)

    def encode(self, data, training=True):
        activations = []
        activations.append(data)

        for i in range(self.num_layers):
            z = cp.dot(activations[-1], self.weights[i]) + self.biases[i]
            # z = self.batch_norms[i].forward(z, training)
            activation = self.relu(z)
            # if training:
            #     activation, mask = self.dropout(activation)   
            activations.append(activation)   
            # self.dropout_masks.append(mask)
        
        self.encoded_data = activations[-1]
        return activations

    def get_encoded_data(self):
        return self.encoded_data
        
    def decode(self, activations, training=True):
        for i in range(self.num_layers, 2 * self.num_layers):
            z = cp.dot(activations[-1], self.weights[i]) + self.biases[i]
            # z = self.batch_norms[i].forward(z, training)
            if not (i == 2 * self.num_layers-1):
                activation = self.relu(z)
            else:
                activation = self.sigmoid(z)
            # if training:
            #     activation, mask = self.dropout(activation)

            activations.append(activation)
            # self.dropout_masks.append(mask)
        self.decoded_data = activations[-1]
        return activations

    def get_decoded_data(self):
        return self.decoded_data

    def calculate_loss(self, in_data, out_data):
        loss = cp.mean(cp.square(in_data - out_data))
        l2_loss = 0.0
        for i in range(len(self.weights)):
            l2_loss += cp.sum(cp.square(self.weights[i]))

        l2_loss = l2_loss * 0.5 * self.reg_lambda
        net_loss = loss + l2_loss
        return net_loss

    def learning_rate_schedule(self, current_epoch, decay_factor=0.1, epochs_decay_threshold=10):
        return self.learning_rate * (decay_factor ** (current_epoch // epochs_decay_threshold))
    
    # def dropout(self, X):
    #     if self.dropout_rate == 0:
    #         return X, None
    #     mask = cp.random.binomial(1, 1 - self.dropout_rate, size=X.shape) / (1 - self.dropout_rate)
    #     return X * mask, mask
    
    def forward_pass(self, data, training=True):
        activations = self.encode(data, training)
        activations = self.decode(activations, training)
        return activations
        
    def backward_pass(self, in_data, activations):
        N = in_data.shape[0]
        err = in_data - self.decoded_data
        dweights = [cp.zeros_like(w) for w in self.weights]
        dbiases = [cp.zeros_like(b) for b in self.biases]
        # dgamma = [cp.zeros_like(bn.gamma) for bn in self.batch_norms]
        # dbeta = [cp.zeros_like(bn.beta) for bn in self.batch_norms]

        #decoder gradients
        for i in range(2 * self.num_layers - 1, self.num_layers - 1, -1):
            if not (i == 2 * self.num_layers - 1):
                dz = self.relu_derivative(activations[i+1]) * activations[i+1]
            else:
                dz =  -err * self.sigmoid_derivative(activations[i+1])
            # if self.dropout_masks[i] is not None:
            #     dz = self.dropout_masks[i] * dz
            # dz, dgamma[i], dbeta[i] = self.batch_norms[i].backward(in_data, dz)
            dweights[i] = cp.dot(activations[i].T, dz) + self.reg_lambda * self.weights[i]
            dbiases[i] = cp.sum(dz, axis=0)

        #encoder gradients
        for i in range(self.num_layers - 1, -1, -1):
            dz = dz = self.relu_derivative(activations[i+1]) * activations[i+1]
            # if self.dropout_masks[i] is not None:
            #     dz = self.dropout_masks[i] * dz
            # dz, dgamma[i], dbeta[i] = self.batch_norms[i].backward(in_data, dz)
            dweights[i] = cp.dot(activations[i].T, dz) + self.reg_lambda * self.weights[i]
            dbiases[i] = cp.sum(dz, axis=0, keepdims=True)

        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * dweights[i]
            self.biases[i] -= self.learning_rate * dbiases[i]
        
        # for i in range(self.num_layers):
        #     self.batch_norms[i].gamma -= self.learning_rate * dgamma[i]
        #     self.batch_norms[i].beta -= self.learning_rate * dbeta[i]

    def train(self, data, v_data, epochs=utility.EPOCHS):
        N = data.shape[0]
        batch_size = 2000
        best_val_loss = float('inf')
        self.train_losses = []
        self.val_losses = []
        gpu_v_data = cp.array(v_data)
        
        #batch gradient decent
        for e in range(epochs):
            # Shuffle data
            # self.learning_rate = self.learning_rate_schedule(e)
            indices = np.arange(N)
            np.random.shuffle(indices)
            data = data.iloc[indices]
            loss = 0

            for i in range(0, N, batch_size):
                batch_data = data[i:i + batch_size]
                gpu_batch_data = cp.array(batch_data)
                activations = self.forward_pass(gpu_batch_data)
                loss += self.calculate_loss(gpu_batch_data, self.decoded_data)
                self.backward_pass(gpu_batch_data, activations)
            
            loss =  loss / (N // batch_size)
            if e == 0 and loss > 1e4:
                print(f"Loss: {loss}")
                print("Terminating")
                return 0
            elif math.isnan(loss):
                print("NAN")
                print("Terminating")
                return 0

            self.train_losses += [cp.asnumpy(loss)]
            self.forward_pass(gpu_v_data)
            val_loss = self.calculate_loss(gpu_v_data, self.decoded_data).item()
            self.val_losses += [cp.asnumpy(val_loss)]

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                self.save_model()

            print(f'Epoch {e+1}/{epochs}, Loss: {loss}')

    def predict(self, data):
        _ = self.forward_pass(data)
        return self.get_decoded_data()
    
    def save_model(self):
        model_params = {}
        for i in range(len(self.weights)):
            model_params[f'W{i+1}'] = cp.asnumpy(self.weights[i])
            model_params[f'b{i+1}'] = cp.asnumpy(self.biases[i])
            # model_params[f'bn_g{i+1}'] = cp.asnumpy(self.batch_norms[i].gamma)
            # model_params[f'bn_b{i+1}'] = cp.asnumpy(self.batch_norms[i].beta)

        file_path = utility.AE_FILE_PATH
        joblib.dump(model_params, file_path)

    def load_model(self):
        file_path = utility.AE_FILE_PATH
        model_params = joblib.load(file_path)
        for i in range(len(self.weights)):
            self.weights[i] = cp.array(model_params[f'W{i+1}'])
            self.biases[i] = cp.array(model_params[f'b{i+1}'])
            # self.batch_norms[i].gamma = cp.array(model_params[f'bn_g{i+1}'])
            # self.batch_norms[i].beta = cp.array(model_params[f'bn_b{i+1}'])