from autoencoder import AutoEncoder
from agent import Agent
import numpy as np
import joblib
import utility
import sys
import matplotlib.pyplot as plt

def get_benign_data(train_data, train_labels):
    indices = np.where(train_labels == 0)[0]
    selected_rows = train_data.iloc[indices]
    return selected_rows

def k_fold_split(data, labels, k):
    # Calculate fold size that is evenly divisible
    data_row_count = data.shape[0]
    fold_size = data_row_count // k  # Drop any remainder for even folds
    usable_count = fold_size * k     # Total samples that fit into k equal folds
    
    # Separate indices by class for stratification
    unique_classes, class_indices = np.unique(labels, return_inverse=True)
    class_folds = {cls: np.array_split(np.where(class_indices == cls)[0][:usable_count], k) for cls in unique_classes}

    # Initialize folds list
    folds = []
    for fold_index in range(k):
        test_indices = np.concatenate([class_folds[cls][fold_index] for cls in unique_classes])
        train_indices = np.concatenate([np.hstack(class_folds[cls][:fold_index] + class_folds[cls][fold_index + 1:]) for cls in unique_classes])
        folds.append((train_indices, test_indices))
    
    return folds

def train_model(ae, train_data, train_labels, valid_data, valid_labels):
    #Because the autoencoder must be trained on benign data exclusively
    ae_train_data = get_benign_data(train_data, train_labels)
    ae_valid_data = get_benign_data(valid_data, valid_labels)
    ae.train(ae_train_data, ae_valid_data)

if __name__ == "__main__":
    input_size = utility.INPUT_DIMENSION
    hidden_sizes = [utility.HIDDEN_DIMENSION, utility.BOTTLENECK_DIMENSION]
    ae = AutoEncoder(input_size, hidden_sizes)
    agent = Agent()
    train_data, train_labels, test_data, test_labels = agent.pipelinea_training_preprocess()

    #Save for rf model training
    data = {
        "train_data": train_data,
        "train_labels": train_labels,
        "test_data": test_data,
        "test_labels": test_labels
    }
    joblib.dump(data, utility.P1_TRAIN_TEST_DATA_PATH)

    #K fold cross validation
    k = 5
    epochs = range(utility.EPOCHS)
    val_losses = []
    train_losses = []
    plt.figure(figsize=(15, 10))
    i = 1
    folds = k_fold_split(train_data, train_labels, k)
    x = -1
    for train_indices, validation_indices in folds:
        X_train, X_valid = train_data.iloc[train_indices], train_data.iloc[validation_indices]
        y_train, y_valid = train_labels.iloc[train_indices], train_labels.iloc[validation_indices]
        train_model(ae, X_train, y_train, X_valid, y_valid)
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