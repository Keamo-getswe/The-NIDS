import matplotlib.pyplot as plt
from agent import Agent
import numpy as np
from sklearn.decomposition import PCA
import utility
import joblib

# To find the best number of components
if __name__ == "__main__":
    agent = Agent()
    X_train, y_train, X_test, y_test = agent.pipelineb_training_preprocess()

    # explained_variance_ratio = pca.explained_variance_ratio_

    # cumulative_explained_variance = np.cumsum(explained_variance_ratio)

    # # Plot the explained variance
    # plt.figure(figsize=(8, 5))
    # plt.bar(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, alpha=0.5, align='center',
    #         label='Individual explained variance')
    # plt.step(range(1, len(cumulative_explained_variance) + 1), cumulative_explained_variance, where='mid',
    #         label='Cumulative explained variance')
    # plt.ylabel('Explained variance ratio')
    # plt.xlabel('Principal components')
    # plt.legend(loc='best')
    # plt.tight_layout()
    # plt.show()