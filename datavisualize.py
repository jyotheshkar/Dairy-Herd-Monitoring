import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# File path
file_path = 'C:/Users/Jyothesh karnam/Desktop/MSc Dissertation/Datasets/Activity Levels CD1.xlsx'

# Load the data
cows_data = pd.read_excel(file_path)

# Check the column names
print(cows_data.columns)

# Convert the date column to datetime (replace 'Date' with the actual column name if different)
cows_data['Date'] = pd.to_datetime(cows_data['Date'], format='%m/%d/%Y')

# Resample the data to weekly (Monday to Sunday) and calculate the mean
cows_data.set_index('Date', inplace=True)
weekly_data = cows_data.resample('W-SUN').mean()

# Prepare data for trend analysis
weekly_data.reset_index(inplace=True)
weekly_data['Week_Number'] = np.arange(len(weekly_data))

# Select one cow ID to plot
cow_id = '6574'

# Perform linear regression for Cow 6574
X_cow = weekly_data[['Week_Number']]
y_cow = weekly_data[cow_id]
model_cow = LinearRegression().fit(X_cow, y_cow)
trend_cow = model_cow.predict(X_cow)

# Perform linear regression for Group mean
y_group = weekly_data['Group mean']
model_group = LinearRegression().fit(X_cow, y_group)
trend_group = model_group.predict(X_cow)

# Calculate the mean and standard deviation of Cow 6574's activity levels
mean_activity = weekly_data[cow_id].mean()
std_activity = weekly_data[cow_id].std()

# Define the threshold levels based on statistical measures
red_line = mean_activity - 2 * std_activity
orange_line = mean_activity - 1 * std_activity
green_line = mean_activity

# Plot the actual data, trend lines, and threshold lines with adjusted styles
plt.figure(figsize=(14, 7))

# Plot for Cow 6574
plt.plot(weekly_data['Date'], y_cow, label=f'Cow {cow_id}')
plt.plot(weekly_data['Date'], trend_cow, label=f'Trend for Cow {cow_id}', linestyle='--')

# Plot for Group mean
plt.plot(weekly_data['Date'], y_group, label='Group mean', color='black')
plt.plot(weekly_data['Date'], trend_group, label='Trend for Group mean', linestyle='--', color='grey')

# Add threshold lines with increased line width
plt.axhline(y=red_line, color='red', linestyle=':', linewidth=2, label='Red line (Not well)')
plt.axhline(y=orange_line, color='orange', linestyle=':', linewidth=2, label='Orange line (Requires medication)')
plt.axhline(y=green_line, color='green', linestyle=':', linewidth=2, label='Green line (Healthy)')

plt.xlabel('Date')
plt.ylabel('Activity Level')
plt.title(f'Trend Analysis of Weekly Activity Levels for Cow {cow_id} and Group Mean with Health Indicators')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
plt.xticks(rotation=45)
plt.tight_layout()

plt.show()

# Print the threshold values
print(f"Red Line (Not well): {red_line}")
print(f"Orange Line (Requires medication): {orange_line}")
print(f"Green Line (Healthy): {green_line}")
