from tensorflow.keras.models import Model
from tensorflow.keras.saving import load_model
from tensorflow.keras.layers import LSTM, Dense, Input, TimeDistributed, RepeatVector, BatchNormalization
from tensorflow.keras import regularizers
from tensorflow.keras.layers import Dropout
from tensorflow.keras.optimizers import Adam
import numpy as np
import utility
import joblib
import matplotlib.pyplot as plt

class LSTMAutoencoder:
    def __init__(self, seq_length=None, num_features=None, latent_dim=8, l2_lambda=0.001, training=True):
        self.sequence_length = seq_length
        self.num_features = num_features
        self.latent_dim = latent_dim
        self.l2_lambda = l2_lambda
        self.threshold = None

        if training:
            if not (self.sequence_length == None) and not (self.num_features == None):
                self.model = self.build_model()
            else:
                self.model = None
        else:
            self.load()

    def build_model(self):
        inputs = Input(shape=(self.sequence_length, self.num_features))

        encoded = LSTM(
            self.latent_dim,
            return_sequences=True,
            kernel_regularizer=regularizers.l2(self.l2_lambda)
        )(inputs)
        encoded = BatchNormalization()(encoded)
        encoded = Dropout(0.2)(encoded)

        encoded = LSTM(
            self.latent_dim // 2,
            return_sequences=True,
            kernel_regularizer=regularizers.l2(self.l2_lambda)
        )(inputs)
        encoded = BatchNormalization()(encoded)
        encoded = Dropout(0.2)(encoded)

        encoded = LSTM(
            self.latent_dim // 4,
            return_sequences=False,
            kernel_regularizer=regularizers.l2(self.l2_lambda)
        )(encoded)
        encoded = BatchNormalization()(encoded)
        encoded = Dropout(0.2)(encoded)

        decoded = RepeatVector(self.sequence_length)(encoded)

        decoded = LSTM(
            self.latent_dim // 4,
            return_sequences=True,
            kernel_regularizer=regularizers.l2(self.l2_lambda)
        )(decoded)
        decoded = BatchNormalization()(decoded)
        decoded = Dropout(0.2)(decoded)

        decoded = LSTM(
            self.latent_dim // 2,
            return_sequences=True,
            kernel_regularizer=regularizers.l2(self.l2_lambda)
        )(decoded)
        decoded = BatchNormalization()(decoded)
        decoded = Dropout(0.2)(decoded)

        decoded = LSTM(
            self.num_features,
            return_sequences=True,
            kernel_regularizer=regularizers.l2(self.l2_lambda)
        )(decoded)
        decoded = BatchNormalization()(decoded)
        decoded = Dropout(0.2)(decoded)

        outputs = TimeDistributed(Dense(self.num_features))(decoded)

        autoencoder = Model(inputs, outputs)
        optimizer = Adam(learning_rate=0.001, clipnorm=1.0)
        autoencoder.compile(optimizer=optimizer, loss='mse')
        return autoencoder

    def train(self, train_data, epochs=50, batch_size=4000):
        history = self.model.fit(train_data, train_data, epochs=epochs, batch_size=batch_size, shuffle=False, validation_split=0.2)
        plt.figure(figsize=(12, 6))
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Training and Validation Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid()
        plt.show()
        self.model.save(utility.LSTM_AE_MODEL_FILE_PATH)
        self.threshold = min(history.history['val_loss'])

        custom_model_params = {
            'sequence_length': self.sequence_length,
            'num_features': self.num_features,
            'latent_dim': self.latent_dim,
            'threshold': self.threshold
        }
        joblib.dump(custom_model_params, utility.LSTM_AE_SUPPORT_FILE_PATH)

    def predict(self, data):
        predicted_data = self.model.predict(data)
        losses = np.mean(np.square(data - predicted_data), axis=(1, 2))
        anomalies = (losses > self.threshold).astype(int)

        return predicted_data, losses, anomalies
    
    def load(self):
        self.model = load_model(utility.LSTM_AE_MODEL_FILE_PATH)
        custom_model_params = joblib.load(utility.LSTM_AE_SUPPORT_FILE_PATH)
        self.sequence_length = custom_model_params['sequence_length']
        self.num_features = custom_model_params['num_features']
        self.latent_dim = custom_model_params['latent_dim']
        self.threshold = custom_model_params['threshold']

