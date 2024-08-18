from autoencoder import AutoEncoder
from agent import Agent
import numpy as np
import joblib
import utility
import os
import matplotlib.pyplot as plt

def get_benign_data(train_data, train_labels):
    indices = np.where(train_labels == 0)[0]
    selected_rows = train_data.iloc[indices]
    return selected_rows

def k_fold_split(data, k):
    data_row_count = data.shape[0]
    indices = np.arange(data_row_count)
    np.random.shuffle(indices)
    fold_sizes = np.full(k, data_row_count // k, dtype=int)

    #Distribute remaining data amongst each of the folds 
    fold_sizes[:data_row_count % k] += 1

    #Current position
    i = 0
    folds = []
    for fold_size in fold_sizes:
        start, stop = i, i + fold_size
        test_indices = indices[start:stop]
        train_indices = np.concatenate([indices[:start], indices[stop:]])
        folds.append((train_indices, test_indices))
        i = stop
    return folds

def train_model(ae, train_data, train_labels, valid_data, valid_labels):
    #Because the autoencoder must be trained on benign data exclusively
    ae_train_data = get_benign_data(train_data, train_labels)
    ae_valid_data = get_benign_data(valid_data, valid_labels)
    ae_train_data = ae_train_data.iloc[:1000]
    ae.train(ae_train_data, ae_valid_data)

if __name__ == "__main__":
    input_size = utility.INPUT_DIMENSION
    hidden_size = utility.HIDDEN_DIMENSION
    ae = AutoEncoder(input_size, hidden_size)
    agent = Agent()
    train_data, train_labels, test_data, test_labels = agent.training_preprocess()
    
    #Save for rf model training
    data = {
        "train_data": train_data,
        "train_labels": train_labels,
        "test_data": test_data,
        "test_labels": test_labels
    }
    joblib.dump(data, utility.TRAIN_TEST_DATA_PATH)

    #K fold cross validation
    k = 5
    epochs = range(utility.EPOCHS)
    val_losses = []
    train_losses = []
    plt.figure(figsize=(15, 10))
    i = 1
    folds = k_fold_split(train_data, k)
    for train_indices, test_indices in folds:
        X_train, X_test = train_data.iloc[train_indices], train_data.iloc[test_indices]
        y_train, y_test = train_labels.iloc[train_indices], train_labels.iloc[test_indices]
        train_model(ae, X_train, y_train, X_test, y_test)
    
        #Plot
        plt.subplot(3, 2, i)
        val_losses += [ae.val_losses]
        train_losses += [ae.train_losses]
        plt.plot(epochs, ae.train_losses, label=f'Training Loss Fold {i}')
        plt.plot(epochs, ae.val_losses, label=f'Validation Error Fold {i}')
        plt.xlabel('Epochs')
        plt.ylabel('Loss/Error')
        plt.title(f'Fold {i}')
        plt.legend()
        i += 1

   
    val_losses = np.array(val_losses)
    train_losses = np.array(train_losses)
    avg_val_loss = np.mean(val_losses, axis=0)
    avg_train_loss = np.mean(train_losses, axis=0)
    # epochs = range(1, epochs + 1)
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.subplot(3, 2, i)
    plt.plot(epochs, avg_train_loss, label='Average Training Loss')
    plt.plot(epochs, avg_val_loss, label='Average Validation Error')
    plt.xlabel('Epochs')
    plt.ylabel('Loss/Error')
    plt.title('Overall Training and Validation Error over Epochs')
    plt.legend()
    plt.show()




