# main.py
import tkinter as tk
from PIL import Image, ImageTk, ImageOps, ImageDraw
import os
import shutil
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt  # Import matplotlib.pyplot here
from leftgraphmain import create_plot
from rightgraphmain import create_right_plot
from results import create_results
from leftbuttons import create_buttons as create_left_buttons
from rightbuttons import create_buttons as create_right_buttons

CONFIG_FILE = 'upload_config.json'
SAVE_DIR = 'saved_upload_data'

def delete_files():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
    if os.path.exists(SAVE_DIR):
        shutil.rmtree(SAVE_DIR)

def center_window(root):
    root.update_idletasks()
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate 90% of screen width and 72% of screen height
    width = int(screen_width * 0.90)
    height = int(screen_height * 0.72)

    # Calculate position x and y coordinates to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f'{width}x{height}+{x}+{y}')
    return screen_width, screen_height

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1,
              x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
              x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
              x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
              x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

# Disable interactive mode
plt.ioff()

# Create the main window
root = tk.Tk()
root.title("Time-series Neural Network Software Suite & App Development For Dairy Herd Monitoring")

# Set the window icon using an image
icon_image_path = os.path.abspath('photo/cowmain.png')  # Replace with the actual path to your image

if os.path.exists(icon_image_path):
    icon_image = ImageTk.PhotoImage(file=icon_image_path)
    root.iconphoto(True, icon_image)
else:
    print(f"Icon image not found at path: {icon_image_path}")

# Set the background color to black
root.configure(bg='black')

# Create a frame for the top content without borders
top_frame = tk.Frame(root, bg='black')
top_frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 10), padx=(10, 10))

# Load and round the image
image_path = os.path.abspath('photo/cowmain.png')  # Ensure you have the image file in the specified path

if os.path.exists(image_path):
    image = Image.open(image_path).convert("RGBA")
    image = image.resize((50, 50), Image.LANCZOS)  # Resize the image
    
    # Create a circular mask
    mask = Image.new('L', (50, 50), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 50, 50), fill=255)
    
    # Apply the mask to the image
    output = ImageOps.fit(image, (50, 50), centering=(0.5, 0.5))
    output.putalpha(mask)
    
    # Ensure transparency is handled correctly
    bg = Image.new("RGBA", output.size, (0, 0, 0, 0))
    bg.paste(output, mask=output)

    image_tk = ImageTk.PhotoImage(bg)

    # Create a label for the image without borders
    image_label = tk.Label(top_frame, image=image_tk, bg='black')
    image_label.grid(row=0, column=0, padx=(0, 10))
else:
    print(f"Image not found at path: {image_path}")

# Create a label for the text "Dairy Herd Monitoring" without borders
text_label = tk.Label(top_frame, text="Dairy Herd Monitoring", bg='black', fg='white', font=("Helvetica", 16))
text_label.grid(row=0, column=1, pady=(6, 0))

# Create a canvas for the "CD1" label with a transparent background and rounded corners
cd1_canvas = tk.Canvas(top_frame, width=80, height=50, bg='black', highlightthickness=0)
cd1_canvas.grid(row=0, column=2, sticky='e', padx=(10, 0), pady=(6, 0))
rounded_rect = create_rounded_rectangle(cd1_canvas, 10, 10, 70, 40, radius=10, fill='white', outline='black')
cd1_canvas.create_text(40, 25, text="CD 1", fill='black', font=("Helvetica", 16))

# Configure grid to expand CD1 Project to the right
top_frame.grid_columnconfigure(2, weight=1)

# Create a frame for the plots without borders
plot_frame = tk.Frame(root, bg='black')
plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(10, 10), pady=(10, 0))

# Create a frame for the left plot without borders
left_plot_frame = tk.Frame(plot_frame, bg='black')
left_plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 1))  # Adjusted padding to increase width

# Create a frame for the right plot without borders
right_plot_frame = tk.Frame(plot_frame, bg='black')
right_plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(1, 5))  # Adjusted padding to increase width

# Create the left plot and embed it in the Tkinter GUI
fig_left = create_plot()
canvas_left = FigureCanvasTkAgg(fig_left, master=left_plot_frame)
canvas_left.draw()
canvas_left.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create the right plot and embed it in the Tkinter GUI
fig_right = create_right_plot()
canvas_right = FigureCanvasTkAgg(fig_right, master=right_plot_frame)
canvas_right.draw()
canvas_right.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Get screen width for setting bottom_frame width
screen_width, screen_height = center_window(root)

# Create a frame for adding bottom spacing without borders
bottom_frame = tk.Frame(root, bg='black', width=int(screen_width * 0.70))
bottom_frame.pack(side=tk.TOP, padx=(10, 10), pady=(10, 10), expand=True)

# Use grid to center the bottom frame
bottom_frame.grid_columnconfigure(1, weight=1)
center_result_frame = tk.Frame(bottom_frame, bg='black')
center_result_frame.grid(row=0, column=1, padx=(5, 5), pady=(0, 0))

# Create results and embed them in the Tkinter GUI
create_results(center_result_frame)

# Create the left buttons and embed them in the Tkinter GUI without borders
left_button_frame = tk.Frame(bottom_frame, bg='black', width=300)
left_button_frame.grid(row=0, column=0, padx=(10, 0), pady=(0, 0), sticky='e')

# Create the right buttons and embed them in the Tkinter GUI without borders
right_button_frame = tk.Frame(bottom_frame, bg='black', width=300)
right_button_frame.grid(row=0, column=2, padx=(0, 10), pady=(0, 0), sticky='w')

create_left_buttons(left_button_frame)
create_right_buttons(right_button_frame)

# Center the window after all widgets are created
center_window(root)

# Set the window to maximized state
root.state('zoomed')

# Bind the delete_files function to the root window's close event
root.protocol("WM_DELETE_WINDOW", lambda: [delete_files(), root.destroy()])

# Run the application
root.mainloop()
