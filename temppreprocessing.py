import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import os

# Common functions
def load_data(file_path):
    try:
        data = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        data = pd.read_csv(file_path, encoding='ISO-8859-1')
    print(f"\nStep 1: Data Collection and Integration - Loaded data from {file_path}.\n")
    return data

def handle_missing_values(df):
    actions_taken = []
    if df.isnull().sum().sum() == 0:
        actions_taken.append("No missing values found. No need for spline interpolation.")
    else:
        missing_percentage = df.isnull().mean() * 100
        if missing_percentage.max() > 30:
            actions_taken.append("Columns with more than 30% missing values found. Consider removing these columns.")
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype in ['float64', 'int64']:
                    df[col].fillna(df[col].interpolate(method='spline', order=3), inplace=True)
                    actions_taken.append(f"Interpolated missing values in column '{col}'.")
    return df, actions_taken

def remove_duplicates(df):
    initial_row_count = df.shape[0]
    df.drop_duplicates(inplace=True)
    final_row_count = df.shape[0]
    return df, initial_row_count - final_row_count

def identify_and_handle_outliers(df):
    actions_taken = []
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    z_scores = (df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std()
    outliers = (z_scores.abs() > 3)
    for col in numeric_cols:
        num_outliers = outliers[col].sum()
        if num_outliers > 0:
            median_value = df[col].median()
            df.loc[outliers[col], col] = median_value.astype(df[col].dtype)
            actions_taken.append(f"Capped {num_outliers} outliers in column '{col}' to median value.")
    return df, actions_taken

def apply_normalization(df):
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = MinMaxScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    scaling_action = "Applied MinMaxScaler for normalization."
    return df, scaling_action

# Function to process temperature data
def process_temperature_data(file_path):
    # Step 1: Load Data
    data = load_data(file_path)

    print("\n")

    # Ensure the first cell of the first column is labeled 'date'
    if data.columns[0] == '' or pd.isna(data.columns[0]):
        data.columns = ['date'] + data.columns[1:].tolist()
    else:
        data.columns = ['date'] + data.columns[1:].tolist() if data.columns[0] != 'date' else data.columns

    # Ensure column names are stripped of leading/trailing spaces
    data.columns = data.columns.str.strip()

    # Step 2: Data Cleaning
    # Handle missing values
    data, missing_actions = handle_missing_values(data)
    print("Step 2: Data Cleaning - Missing Values")
    for action in missing_actions:
        print(action)

    print("\n")

    # Remove duplicates
    data, num_duplicates_removed = remove_duplicates(data)
    print(f"Removed {num_duplicates_removed} duplicate rows.")

    print("\n")

    # Identify and handle outliers
    data, outlier_actions = identify_and_handle_outliers(data)
    print("Step 2: Data Cleaning - Outliers")
    for action in outlier_actions:
        print(action)

    print("\n\n")

    # Step 3: Data Transformation
    data_transformed, scaling_action = apply_normalization(data)
    print("Step 3: Data Transformation")
    print(scaling_action)

    print("\n\n")

    # Display final DataFrame
    print("Final DataFrame preview:")
    columns_to_display = list(data_transformed.columns[:6]) + ["..."] + list(data_transformed.columns[-6:])
    df_preview = data_transformed[data_transformed.columns[:6]].copy()
    df_preview["..."] = "..."
    for col in data_transformed.columns[-6:]:
        df_preview[col] = data_transformed[col]
    print(df_preview.head().to_string(index=False))

    print("\n\n")

    # Save the cleaned and transformed data
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop_path, "preprocessed_data")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created folder: {folder_path}")
    
    output_filename = 'preprocessed_temperature_data.csv'
    output_path = os.path.join(folder_path, output_filename)
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"Deleted existing file: {output_path}")
    data_transformed.to_csv(output_path, index=False)
    print(f"Processed file saved at: {output_path}")

    print("\n\n" + "-"*50 + "\n\n")

# Example usage
temperature_file_path = 'C:/Users/Jyothesh karnam/Desktop/Trail/TrailTemp.csv'
process_temperature_data(temperature_file_path)
