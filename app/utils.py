def generate_random_features():
    """
    Generate random features for a normal transaction.
    Values are sampled from a uniform distribution between -2 and 2,
    which is typical for non-fraudulent transactions in PCA-transformed datasets.
    """
    return {f"V{i}": float(np.random.uniform(-2, 2)) for i in range(1, 29)}

def generate_fraud_prone_features():
    """
    Generate features more likely to be associated with fraud (outliers).
    Most features are sampled from a normal range, but some are set as outliers
    (much higher or lower values), mimicking the behavior of fraudulent transactions.
    """
    features = {}
    for i in range(1, 29):
        # 80% chance to be a normal value, 20% chance to be an outlier
        if np.random.rand() < 0.8:
            features[f"V{i}"] = float(np.random.uniform(-2, 2))
        else:
            # Outlier: much higher or lower value
            features[f"V{i}"] = float(np.random.uniform(-10, 10))
    return features