import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

def plot_temperature_levels(cow_id, compare_with_cow_id=None, file_path=None):
    # Load the dataset with specified encoding
    try:
        data = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        data = pd.read_csv(file_path, encoding='ISO-8859-1')  # Try an alternative encoding

    # Extracting data for the specified cow ID and Group mean
    columns_to_extract = ['Unnamed: 0', str(cow_id)]
    if compare_with_cow_id:
        columns_to_extract.append(str(compare_with_cow_id))
    
    # Assume the last column is always 'Group mean'
    group_mean_column = data.columns[-1]
    columns_to_extract.append(group_mean_column)
    
    cow_data = data[columns_to_extract].copy()
    new_column_names = ['Date', 'Temperature'] + ([f'Cow {compare_with_cow_id} Temperature'] if compare_with_cow_id else []) + ['Group Mean']
    cow_data.columns = new_column_names

    # Converting 'Date' to datetime format using .loc to avoid SettingWithCopyWarning
    cow_data['Date'] = pd.to_datetime(cow_data['Date'])

    # Calculate the week number from the start date
    cow_data['Week Number'] = ((cow_data['Date'] - cow_data['Date'].min()).dt.days // 7) + 1

    # Plotting the temperature levels and group mean temperature levels over time
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot the lines
    cow_line, = ax.plot(cow_data['Date'], cow_data['Temperature'], linestyle='-', label=f'Cow {cow_id} Temperature Data', color='#0000FF', linewidth=2.5)
    group_line, = ax.plot(cow_data['Date'], cow_data['Group Mean'], linestyle='-', label='Entire Cow Herd Temperature Data', color='red')
    
    if compare_with_cow_id:
        compare_line, = ax.plot(cow_data['Date'], cow_data[f'Cow {compare_with_cow_id} Temperature'], linestyle='-', label=f'Cow {compare_with_cow_id} Temperature Data', color='lime')

    # Plot the markers
    cow_marker = ax.scatter(cow_data['Date'], cow_data['Temperature'], color='#0000FF', s=50, label=f'Cow {cow_id} Temperature Data')
    group_marker = ax.scatter(cow_data['Date'], cow_data['Group Mean'], color='red', s=50, label='Entire Cow Herd Temperature Data')
    
    if compare_with_cow_id:
        compare_marker = ax.scatter(cow_data['Date'], cow_data[f'Cow {compare_with_cow_id} Temperature'], color='lime', s=50, label=f'Cow {compare_with_cow_id} Temperature Data')

    # Set the title with the appropriate comparison
    title = f'Temperature Levels of Cow ID {cow_id} vs Entire Cow Herd Temperature Data'
    if compare_with_cow_id:
        title += f' vs Cow ID {compare_with_cow_id}'
    ax.set_title(title)
    
    ax.set_xlabel('Week Number')
    ax.set_ylabel('Temperature')
    ax.grid(True, color='gray')

    # Setting x-ticks to weekly intervals and labeling them as "Week 1", "Week 2", etc.
    week_numbers = cow_data['Week Number'].unique()
    week_labels = [f'Week {int(week)}' for week in week_numbers]
    week_dates = cow_data['Date'].iloc[::7]  # Selects a date every week for the tick locations
    ax.set_xticks(week_dates)
    ax.set_xticklabels(week_labels, rotation=45)

    # Customizing the legend
    handles, labels = ax.get_legend_handles_labels()
    # Filtering out scatter plot legends
    handles = [handles[0], handles[1]] + ([handles[2]] if compare_with_cow_id else [])
    labels = [labels[0], labels[1]] + ([labels[2]] if compare_with_cow_id else [])
    ax.legend(handles, labels)

    plt.tight_layout()

    # Define tooltip labels for each marker
    tooltip_labels = {
        cow_marker: f'Cow {cow_id} Temperature Data',
        group_marker: 'Entire Cow Herd Temperature Data',
    }
    if compare_with_cow_id:
        tooltip_labels[compare_marker] = f'Cow {compare_with_cow_id} Temperature Data'

    # Adding tooltips to data points only
    cursor = mplcursors.cursor([cow_marker, group_marker] + ([compare_marker] if compare_with_cow_id else []), hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(
        f'{tooltip_labels[sel.artist]}:\nDate: {cow_data["Date"].iloc[int(sel.index)].strftime("%Y-%m-%d")}\nTemperature: {sel.target[1]:.2f}'
    ))
    cursor.connect("add", lambda sel: sel.annotation.get_bbox_patch().set(
        boxstyle="round,pad=0.3", edgecolor=sel.artist.get_edgecolor(), facecolor='black', alpha=1
    ))
    cursor.connect("add", lambda sel: sel.annotation.arrow_patch.set(
        arrowstyle='-|>', color='white'
    ))

    # Show the plot with interactive features
    plt.show()

# Example usage
file_path = 'C:/Users/Jyothesh karnam/Desktop/Trail/trailTemp.csv'
cow_id = input("Enter cow ID: ")

# Asking the user if they want to compare with another cow
compare_option = input("Do you want to compare with another cow? (yes/no): ").strip().lower()

compare_with_cow_id = None
if compare_option == 'yes':
    compare_with_cow_id = input("Enter another cow ID to compare with: ")

plot_temperature_levels(cow_id, compare_with_cow_id, file_path)
