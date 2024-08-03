# activity.py
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

def plot_activity_levels(cow_id, compare_with_cow_id=None, file_path=None):
    # Close any previously opened figures
    plt.close('all')

    # Load the dataset with specified encoding
    try:
        data = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        data = pd.read_csv(file_path, encoding='ISO-8859-1')  # Try an alternative encoding

    # Extracting data for the specified cow ID and Group mean
    columns_to_extract = ['Unnamed: 0', str(cow_id), 'Group mean']
    if compare_with_cow_id:
        columns_to_extract.append(str(compare_with_cow_id))
    cow_data = data[columns_to_extract].copy()
    cow_data.columns = ['Date', 'Activity Level', 'Entire Cow Herd Activity Level'] + ([f'Cow {compare_with_cow_id} Activity Level'] if compare_with_cow_id else [])

    # Converting 'Date' to datetime format using .loc to avoid SettingWithCopyWarning
    cow_data['Date'] = pd.to_datetime(cow_data['Date'])

    # Calculate the week number from the start date
    cow_data['Week Number'] = ((cow_data['Date'] - cow_data['Date'].min()).dt.days // 7) + 1

    # Plotting the activity levels and group mean activity levels over time
    plt.style.use('dark_background')

    # Plot for the main cow ID
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    cow_line, = ax1.plot(cow_data['Date'], cow_data['Activity Level'], linestyle='-', label=f'Cow {cow_id} Activity Level', color='blue')
    group_line, = ax1.plot(cow_data['Date'], cow_data['Entire Cow Herd Activity Level'], linestyle='-', label='Entire Cow Herd Activity Level', color='red')

    cow_marker = ax1.scatter(cow_data['Date'], cow_data['Activity Level'], color='blue', s=50, label=f'Cow {cow_id} Activity Level')
    group_marker = ax1.scatter(cow_data['Date'], cow_data['Entire Cow Herd Activity Level'], color='red', s=50, label='Entire Cow Herd Activity Level')

    ax1.set_title(f'Activity Levels of Cow ID {cow_id} vs Entire Cow Herd Activity Level')
    ax1.set_xlabel('Week Number')
    ax1.set_ylabel('Activity Level')
    ax1.grid(True, color='gray')

    week_numbers = cow_data['Week Number'].unique()
    week_labels = [f'Week {int(week)}' for week in week_numbers]
    week_dates = cow_data['Date'].iloc[::7]
    ax1.set_xticks(week_dates)
    ax1.set_xticklabels(week_labels, rotation=45)

    handles, labels = ax1.get_legend_handles_labels()
    handles = [handles[0], handles[1]]
    labels = [labels[0], labels[1]]
    ax1.legend(handles, labels)

    plt.tight_layout()

    tooltip_labels = {
        cow_marker: f'Cow {cow_id} Activity Level',
        group_marker: 'Entire Cow Herd Activity Level',
    }

    cursor1 = mplcursors.cursor([cow_marker, group_marker], hover=True)
    cursor1.connect("add", lambda sel: sel.annotation.set_text(
        f'{tooltip_labels[sel.artist]}:\nDate: {cow_data["Date"].iloc[int(sel.index)].strftime("%Y-%m-%d")}\nActivity Level: {sel.target[1]:.2f}'
    ))
    cursor1.connect("add", lambda sel: sel.annotation.get_bbox_patch().set(
        boxstyle="round,pad=0.3", edgecolor=sel.artist.get_edgecolor(), facecolor='black', alpha=1
    ))
    cursor1.connect("add", lambda sel: sel.annotation.arrow_patch.set(
        arrowstyle='-|>', color='white'
    ))

    # Show the first plot
    fig1.show()

    if compare_with_cow_id:
        # Plot for the comparison
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        cow_line, = ax2.plot(cow_data['Date'], cow_data['Activity Level'], linestyle='-', label=f'Cow {cow_id} Activity Level', color='blue')
        compare_line, = ax2.plot(cow_data['Date'], cow_data[f'Cow {compare_with_cow_id} Activity Level'], linestyle='-', label=f'Cow {compare_with_cow_id} Activity Level', color='lime')
        group_line, = ax2.plot(cow_data['Date'], cow_data['Entire Cow Herd Activity Level'], linestyle='-', label='Entire Cow Herd Activity Level', color='red')

        cow_marker = ax2.scatter(cow_data['Date'], cow_data['Activity Level'], color='blue', s=50, label=f'Cow {cow_id} Activity Level')
        compare_marker = ax2.scatter(cow_data['Date'], cow_data[f'Cow {compare_with_cow_id} Activity Level'], color='lime', s=50, label=f'Cow {compare_with_cow_id} Activity Level')
        group_marker = ax2.scatter(cow_data['Date'], cow_data['Entire Cow Herd Activity Level'], color='red', s=50, label='Entire Cow Herd Activity Level')

        ax2.set_title(f'Activity Levels of Cow ID {cow_id} vs Entire Cow Herd Activity Level vs Cow ID {compare_with_cow_id}')
        ax2.set_xlabel('Week Number')
        ax2.set_ylabel('Activity Level')
        ax2.grid(True, color='gray')

        week_numbers = cow_data['Week Number'].unique()
        week_labels = [f'Week {int(week)}' for week in week_numbers]
        week_dates = cow_data['Date'].iloc[::7]
        ax2.set_xticks(week_dates)
        ax2.set_xticklabels(week_labels, rotation=45)

        handles, labels = ax2.get_legend_handles_labels()
        handles = [handles[0], handles[1], handles[2]]
        labels = [labels[0], labels[1], labels[2]]
        ax2.legend(handles, labels)

        plt.tight_layout()

        tooltip_labels = {
            cow_marker: f'Cow {cow_id} Activity Level',
            group_marker: 'Entire Cow Herd Activity Level',
            compare_marker: f'Cow {compare_with_cow_id} Activity Level'
        }

        cursor2 = mplcursors.cursor([cow_marker, group_marker, compare_marker], hover=True)
        cursor2.connect("add", lambda sel: sel.annotation.set_text(
            f'{tooltip_labels[sel.artist]}:\nDate: {cow_data["Date"].iloc[int(sel.index)].strftime("%Y-%m-%d")}\nActivity Level: {sel.target[1]:.2f}'
        ))
        cursor2.connect("add", lambda sel: sel.annotation.get_bbox_patch().set(
            boxstyle="round,pad=0.3", edgecolor=sel.artist.get_edgecolor(), facecolor='black', alpha=1
        ))
        cursor2.connect("add", lambda sel: sel.annotation.arrow_patch.set(
            arrowstyle='-|>', color='white'
        ))

        # Show the second plot
        fig2.show()
