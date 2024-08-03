import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

def create_results(parent_frame):
    # Data to plot
    labels = ['Red Alert', 'Orange Alert', 'Green Alert']
    sizes = [1/3, 1/3, 1/3]  # Equal sizes
    colors = ['black', 'black', 'black']
    explode = (0, 0, 0)  # explode a slice if required

    # Custom autopct to display 0% instead of the actual percentage
    def custom_autopct(pct):
        return '0%' if pct > 0 else ''

    # Create the pie chart
    fig, ax = plt.subplots(figsize=(3, 3))  # Increased the size of the figure
    fig.patch.set_facecolor('black')  # Set the background color to black
    ax.set_facecolor('black')  # Set the axes background color to black

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=custom_autopct,
                                      shadow=True, startangle=90, textprops={'color': 'white', 'fontsize': 6})  # Reduced text size

    # Draw the borders between slices
    for i, wedge in enumerate(wedges):
        theta1, theta2 = wedge.theta1, wedge.theta2
        center, r = wedge.center, wedge.r
        x = [center[0], center[0] + r * np.cos(np.radians(theta1))]
        y = [center[1], center[1] + r * np.sin(np.radians(theta1))]
        ax.plot(x, y, color='white', linewidth=1.5)

        x = [center[0], center[0] + r * np.cos(np.radians(theta2))]
        y = [center[1], center[1] + r * np.sin(np.radians(theta2))]
        ax.plot(x, y, color='white', linewidth=1.5)

    # Draw the dividing lines
    for i in range(3):
        angle = 90 + i * 120
        x = [0, r * np.cos(np.radians(angle))]
        y = [0, r * np.sin(np.radians(angle))]
        ax.plot(x, y, color='white', linewidth=1.5)

    # Draw the outer circle of the pie chart
    outer_circle = plt.Circle((0, 0), r, color='white', fill=False, linewidth=2)
    ax.add_artist(outer_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')

    # Create a frame for the chart and button
    result_frame = tk.Frame(parent_frame, bg='black')
    result_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add the pie chart to the Tkinter window
    chart_frame = tk.Frame(result_frame, bg='black')
    chart_frame.grid(row=0, column=0, pady=(0, 5))  # Adjust padding as needed
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)  # A tk.DrawingArea
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Function to show a popup message
    def show_alert_message():
        alert_button.config(highlightbackground='black')
        alert_window = tk.Toplevel(parent_frame)
        alert_window.title("Alert")
        alert_window.configure(bg='black')
        alert_window.geometry("200x100")

        # Center the popup window in the main window
        parent_frame.update_idletasks()
        x = parent_frame.winfo_x() + (parent_frame.winfo_width() // 2) - (alert_window.winfo_reqwidth() // 2)
        y = parent_frame.winfo_y() + (parent_frame.winfo_height() // 2) - (alert_window.winfo_reqheight() // 2)
        alert_window.geometry(f'+{x}+{y}')

        message_label = tk.Label(alert_window, text="Default Message", bg='black', fg='white', font=("Helvetica", 12))
        message_label.pack(expand=True)

    # Create a frame for the buttons
    button_frame = tk.Frame(result_frame, bg='black')
    button_frame.grid(row=1, column=0)  # Center the button exactly below the pie chart

    # Button configuration for the "Alert Metrics" button
    alert_button = tk.Button(button_frame, text="Alert Metrics", bg='white', fg='black', font=("Helvetica", 12),
                             width=14, height=2, bd=2, relief="solid", activebackground='black', activeforeground='white',
                             highlightbackground='green', highlightcolor='green', borderwidth=2)
    
    # Arrange the button in the frame
    alert_button.pack(pady=(0, 0))  # Adjust padding as needed

    # Bind the click event to show the alert message
    alert_button.config(command=show_alert_message)

# Ensure this part runs only when executing this file directly
if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()
    root.title("Pie Chart Example")
    root.configure(bg='black')

    # Create the results frame
    create_results(root)

    # Start the Tkinter event loop
    root.mainloop()
