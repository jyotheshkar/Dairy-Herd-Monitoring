import numpy as np

# Load the saved sequences, targets, and dates
X_activity = np.load('X_activity.npy')
y_activity = np.load('y_activity.npy')
sequence_dates = np.load('sequence_dates.npy', allow_pickle=True)

# Step 5: Train-Test Split

def train_test_split_temporal(X, y, test_size=0.2):
    """
    Splits the data into training and test sets based on a temporal split.

    Parameters:
    - X: numpy array of shape (num_sequences, sequence_length, num_features) containing the sequences.
    - y: numpy array of shape (num_sequences, num_features) containing the targets.
    - test_size: float, proportion of the dataset to include in the test split (default is 0.2).

    Returns:
    - X_train: numpy array containing the training sequences.
    - X_test: numpy array containing the test sequences.
    - y_train: numpy array containing the training targets.
    - y_test: numpy array containing the test targets.
    """
    split_index = int(len(X) * (1 - test_size))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    return X_train, X_test, y_train, y_test

# Determine split ratio (e.g., 80% training, 20% testing)
test_size = 0.2

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split_temporal(X_activity, y_activity, test_size)

# Verify the split
print(f"Training sequences: {X_train.shape}, Training targets: {y_train.shape}")
print(f"Test sequences: {X_test.shape}, Test targets: {y_test.shape}")

# Check date ranges for training and test sets
train_dates = [seq[0] for seq in sequence_dates[:len(X_train)]]
test_dates = [seq[0] for seq in sequence_dates[len(X_train):]]
print(f"Training set date range: {train_dates[0]} to {train_dates[-1]}")
print(f"Test set date range: {test_dates[0]} to {test_dates[-1]}")
