import numpy as np
import pandas as pd

# Load the data
activity_data = pd.read_csv('C:/Users/Jyothesh karnam/Desktop/preprocessed_data/preprocessed_activity_data.csv')

# Ensure column names are stripped of leading/trailing spaces
activity_data.columns = activity_data.columns.str.strip()

# Print the column names to check for 'date'
print("Column names in the dataset:", activity_data.columns.tolist())

# Store header row (metadata)
metadata = activity_data.columns.tolist()  # ['date', '6774', '6775', ..., '6829', 'Group mean']

# Store dates column
dates = activity_data['date'].tolist()

# Exclude the date column for training data
activity_data = activity_data.drop(columns=['date'])

# Print the number of rows and columns
num_rows, num_columns = activity_data.shape
print(f"Number of rows: {num_rows}, Number of columns: {num_columns}")

def determine_dynamic_sequence_length(data, min_proportion=0.1, max_proportion=0.5, min_length=5, max_length=30):
    """
    Determines a dynamic sequence length based on the data characteristics and dynamic bounding.

    Parameters:
    - data: pandas DataFrame containing the preprocessed data.
    - min_proportion: float, the minimum proportion of the dataset size to consider for the minimum length.
    - max_proportion: float, the maximum proportion of the dataset size to consider for the maximum length.
    - min_length: int, the minimum sequence length to consider.
    - max_length: int, the maximum sequence length to consider.

    Returns:
    - sequence_length: int, the determined sequence length.
    """
    data_length = len(data)  # Get the number of rows in the dataset
    # Calculate the sequence length as the square root of the data length
    sequence_length = int(np.sqrt(data_length))
    
    # Calculate dynamic bounds based on proportions of the dataset size
    dynamic_min_length = max(min_length, int(data_length * min_proportion))
    dynamic_max_length = min(max_length, int(data_length * max_proportion))
    
    # Ensure the sequence length is within the dynamically determined bounds
    sequence_length = max(dynamic_min_length, min(sequence_length, dynamic_max_length))
    
    return sequence_length

def create_activity_sequences(activity_data, sequence_length):
    """
    Creates overlapping sequences and corresponding targets from the activity data.

    Parameters:
    - activity_data: pandas DataFrame containing the preprocessed activity data.
    - sequence_length: int, the length of each sequence.

    Returns:
    - X_activity: numpy array of shape (num_sequences, sequence_length, num_features) containing the sequences.
    - y_activity: numpy array of shape (num_sequences, num_features) containing the targets.
    - sequence_dates: list of lists containing dates for each sequence
    """
    X_activity = []
    y_activity = []
    sequence_dates = []
    
    for i in range(len(activity_data) - sequence_length):
        seq = activity_data.iloc[i:i + sequence_length, :].values  # Include all columns except the date
        target = activity_data.iloc[i + sequence_length, :].values  # Include all columns except the date
        dates_seq = dates[i:i + sequence_length]  # Extract dates corresponding to the sequence
        X_activity.append(seq)
        y_activity.append(target)
        sequence_dates.append(dates_seq)
        
    return np.array(X_activity), np.array(y_activity), sequence_dates

# Determine sequence length dynamically
sequence_length = determine_dynamic_sequence_length(activity_data)  
print(f"Determined sequence length for activity data: {sequence_length}")

# Create input sequences and target variables
X_activity, y_activity, sequence_dates = create_activity_sequences(activity_data, sequence_length)

# Display the final shapes and the steps taken
print(f"Activity data sequences: {X_activity.shape}, Targets: {y_activity.shape}")

# Print the columns included in the sequences to verify only the date column is excluded
print("\nColumns included in sequences:")
print(activity_data.columns.tolist())  # Exclude only 'date' column

# Print the steps and decisions taken
print("\nSteps and decisions taken:")
print("1. Loaded the preprocessed activity data.")
print("2. Stripped leading/trailing spaces from column names.")
print("3. Stored metadata (column names) and dates separately.")
print("4. Excluded the date column for training data.")
print(f"5. Determined sequence length dynamically based on data size: {num_rows} rows.")
print(f"6. Calculated sequence length using square root heuristic: {int(np.sqrt(num_rows))}.")
print(f"7. Applied dynamic bounds: min_length={max(5, int(num_rows * 0.1))}, max_length={min(30, int(num_rows * 0.5))}.")
print(f"8. Final sequence length after applying bounds: {sequence_length}.")
print("9. Created overlapping sequences and corresponding targets.")
print(f"   - Number of sequences created: {X_activity.shape[0]}")
print(f"   - Sequence length: {sequence_length}")
print(f"   - Number of features in each sequence: {X_activity.shape[2]}")
print(f"   - Example of the first sequence (showing first row of the first sequence): {X_activity[0][0]}")
print(f"   - Example of the first target (showing the target values for the first sequence): {y_activity[0]}")
