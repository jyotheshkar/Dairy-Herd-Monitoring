import matplotlib.pyplot as plt
import numpy as np

def create_right_plot():
    # Generate the plot
    fig, ax = plt.subplots(figsize=(8.05, 5))  # Increased width by 15%
    fig.patch.set_facecolor('black')  # Set the background color to black
    ax.set_facecolor('black')  # Set the axes background color to black

    # Customize the axes
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    # Set the axis labels with white color
    ax.set_xlabel('X-axis', color='white')
    ax.set_ylabel('Y-axis', color='white')

    # Set x and y axis limits
    ax.set_xlim([0, 8])
    ax.set_ylim([0, 8])

    # Set x and y axis ticks to integers
    ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))

    # Add grid lines in darker gray
    ax.grid(True, which='both', color='#444444', linestyle='--', linewidth=0.5)

    return fig

# Create the empty plot
fig = create_right_plot()
plt.show()
