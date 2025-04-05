# Repository Disclaimer

This codebase was developed as part of a university project and is intended for academic and research purposes only. It is not optimized for real-world deployment and should not be used in a live environment. The project lacks rigorous security and performance optimizations necessary for production-grade intrusion detection systems. Users should exercise caution when experimenting with the code and consider further improvements before practical implementation.

# Introduction

As cyber threats continue to evolve, intrusion detection systems (IDS) play a critical role in identifying and mitigating network attacks. Traditional signature-based IDS solutions struggle against zero-day attacks due to their reliance on predefined attack patterns. In contrast, anomaly-based IDS methods use machine learning (ML) to identify deviations from normal network behavior, making them more adaptable to emerging threats. This research investigates the use of semi-supervised ML techniques for network anomaly detection, focusing on feature engineering and classification performance.

# Research Objectives

This study seeks to evaluate the performance of semi-supervised learning techniques in a general network environment. Specifically, it aims to determine whether the intrusion detection solution proposed by [Durga and Mangla](https://pdfs.semanticscholar.org/8131/c35730089a8110a7354dcc462a673414736d.pdf) can achieve comparable results on the CICIDS2017 dataset. Furthermore, it assesses how this experiment performs against the semi-supervised approach proposed by [Lutsiv et al.](https://doi.org/10.32604/cmc.2022.018773) on the same dataset.

# Methodology

Two ML-based IDS pipelines were developed and evaluated using the CICIDS2017 dataset:

Pipeline A: Utilizes an autoencoder for feature engineering followed by a random forest classifier for anomaly detection.

Pipeline B: Applies Principal Component Analysis (PCA) for feature selection and dimensionality reduction, and employs an LSTM autoencoder for anomaly detection.

Both pipelines integrate into a simplified IDS framework with three components:

Agent (Preprocessing): Handles missing values, standardizes data, and addresses class imbalances via SMOTE.

Director (Feature Engineering & Anomaly Detection): Processes and detects network anomalies.

Notifier (Visualization): Displays anomaly detection results for user analysis.

# Experiment

Pipeline A trains an autoencoder exclusively on benign traffic to extract a latent feature representation, which is then used by the random forest classifier to classify normal and malicious traffic. The model is optimized using L2 regularization, batch normalization, and stochastic gradient descent. Due to computational constraints, adjustments were made to improve processing efficiency. The class imbalance issue was partially mitigated using a combination of random undersampling and SMOTE oversampling, although the dataset remained skewed.

Pipeline B preprocesses raw network traffic for time-series analysis, removes null values, applies PCA to retain 98% variance, and organizes data into sequences for LSTM input. The LSTM autoencoder encodes and decodes temporal patterns, detecting anomalies based on reconstruction errors exceeding a predefined threshold. It is optimized using L2 regularization, batch normalization, dropout, and the Adam optimizer with gradient clipping. Unlike Pipeline A, oversampling in time-series data was challenging, making it difficult to effectively balance the dataset.

Both pipelines are evaluated using precision, recall, F1-score, and specificity to mitigate the misleading effects of accuracy in imbalanced datasets.

# Results and Findings

Pipeline A achieved an F1-score of 0.711, with precision of 0.856 and recall of 0.609. The high precision indicates that benign traffic was correctly classified at a high rate, while the lower recall suggests that many malicious instances were misclassified as benign. This is attributed to the autoencoder being trained only on benign traffic and the weighting of this imbalanced data leading to poor attack identification. Subsequently, the random forest classifier’s reliance on these inadequate compressed latent features may have contributed to its struggles in distinguishing subtle attack variations.

Pipeline B achieved an F1-score of 0.682, with precision of 0.743 and recall of 0.627. The lower precision compared to Pipeline A suggests an increased false positive rate, likely due to the PCA reducing feature space in a way that may have discarded valuable distinguishing features. However, the slightly higher recall indicates that Pipeline B was marginally better at detecting malicious traffic, benefiting from the sequential nature of LSTM, which captures time-dependent attack behaviors. The challenges in handling class imbalance in time-series data contributed to a higher false positive rate, affecting specificity.

In terms of feature engineering, L2 regularization outperformed batch normalization in stabilizing training, reinforcing the importance of careful hyperparameter selection in both pipelines. The use of PCA in Pipeline B, while effective for dimensionality reduction, may have removed key features needed for attack detection. Both pipelines struggled with class imbalance, affecting detection rates for minority classes. Pipeline A misclassified malicious traffic as benign due to the autoencoder’s training approach, while Pipeline B exhibited bias toward benign traffic, resulting in poor specificity.

# Limitations and Future Work

Several challenges limited the scope of this research. Hyperparameter optimization was constrained by time limitations, leading to suboptimal parameter selection. Given the complexity of the models, techniques such as grid search or Bayesian optimization could have significantly improved performance but were impractical within the available time frame. Computational constraints also played a significant role, restricting the dataset size and model training duration. Training deep learning models, especially for time-series data in Pipeline B, required substantial computational resources that were not available, limiting the depth and complexity of hyperparameter tuning and model architecture.

Further experimentation is needed to refine sampling techniques for better anomaly detection, especially for time-series data in Pipeline B. Oversampling strategies need to be adjusted for sequential data to ensure balanced training. Additionally, alternative techniques such as weighted loss functions or cost-sensitive learning could be explored to mitigate the impact of class imbalance. The use of PCA in Pipeline B helped reduce feature dimensionality but may have discarded important discriminative features, affecting classification performance. Further experimentation with alternative feature selection techniques, such as mutual information or deep feature extraction, could yield better results.

Reproducibility challenges also emerged due to the lack of detailed methodology descriptions in the papers used for comparison, which introduced difficulties in replicating their results. This highlights the importance of detailed reporting in machine learning research to ensure fair and meaningful comparisons. Future work will explore automated hyperparameter optimization, alternative semi-supervised techniques, and real-time IDS deployment strategies. Additionally, the integration of explainable AI (XAI) methods could provide insights into model decisions and improve interpretability.

# Conclusion

This study demonstrates the potential of semi-supervised ML techniques for network anomaly detection. While both pipelines effectively reduced feature space and improved classification accuracy, handling class imbalance remains a significant challenge. Pipeline A provided a more stable classifier for static network traffic, while Pipeline B leveraged temporal dependencies but suffered from oversampling limitations. The results indicate that while semi-supervised methods can enhance IDS performance, further refinements in data preprocessing, feature selection, and class balancing are necessary for robust and reliable anomaly detection. Future work should focus on improving class balance strategies and exploring more adaptive feature extraction techniques for real-time network environments.

