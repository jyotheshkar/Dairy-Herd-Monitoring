# visualizebutton.py
import tkinter as tk
from tkinter import messagebox
from utils import custom_error_messagebox, custom_visualize_messagebox
from activity import plot_activity_levels  # Importing the backend function

class VisualizeDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualize Data")
        self.root.configure(bg='black')  # Set the window background to black

        self.main_frame = tk.Frame(self.root, bg='black')
        self.main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.create_visualize_interface()

        self.center_window(600, 300, 180)  # Adjusted the x_offset to move the window slightly to the right

    def button_style(self):
        return {
            'bg': '#555555',  # Button background color
            'fg': 'white',    # Button text color
            'font': ('Helvetica', 11),  # Font style same as upload buttons
            'activebackground': '#777777',  # Button background color when clicked
            'activeforeground': 'white',  # Button text color when clicked
            'bd': 0,  # No border
            'highlightthickness': 2,
            'highlightcolor': 'blue',
            'highlightbackground': 'blue',
            'width': 25,  # Width of the button
            'height': 2   # Height of the button
        }

    def create_visualize_interface(self):
        label = tk.Label(self.main_frame, text="Cow ID Number:", bg='black', fg='white', font=('Helvetica', 11))
        label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

        vcmd = (self.root.register(self.validate_cow_id), '%P')
        self.cow_id_entry = tk.Entry(self.main_frame, font=('Helvetica', 11), width=20, validate='key', validatecommand=vcmd)
        self.cow_id_entry.grid(row=0, column=1, padx=10, pady=10, ipady=5, sticky=tk.W)

        self.visualize_activity_button = tk.Button(self.main_frame, text="Visualize Daily Activity Data", command=self.visualize_activity_data, **self.button_style())
        self.visualize_activity_button.grid(row=1, column=0, padx=10, pady=(10, 0))  # Added vertical padding

        self.visualize_temperature_button = tk.Button(self.main_frame, text="Visualize Temperature Data", command=self.visualize_temperature_data, **self.button_style())
        self.visualize_temperature_button.grid(row=1, column=1, padx=10, pady=(10, 0))  # Added vertical padding

        self.visualize_button = tk.Button(self.main_frame, text="Visualize", command=self.show_compare_dialog, bg='#2e8b57', fg='white', font=('Helvetica', 11, 'bold'), width=10, height=2, bd=0, highlightthickness=0)
        self.visualize_button.grid(row=2, column=0, columnspan=2, pady=(20, 10))  # Added vertical padding

        self.data_type = None

    def validate_cow_id(self, P):
        if P.isdigit() and len(P) <= 4:
            return True
        elif P == "":
            return True
        else:
            return False

    def visualize_activity_data(self):
        cow_id = self.cow_id_entry.get()
        if not cow_id:
            custom_error_messagebox("Error", "Please enter a Cow ID number.", self.root)
            return
        self.data_type = "activity"
        self.show_compare_dialog()

    def visualize_temperature_data(self):
        cow_id = self.cow_id_entry.get()
        if not cow_id:
            custom_error_messagebox("Error", "Please enter a Cow ID number.", self.root)
            return
        self.data_type = "temperature"
        self.visualize_data()

    def show_compare_dialog(self):
        cow_id = self.cow_id_entry.get()
        if not cow_id:
            custom_error_messagebox("Error", "Please enter a Cow ID number.", self.root)
            return
        custom_visualize_messagebox("Visualize", f"Visualizing {self.data_type} data for Cow ID: {cow_id}", self.root, self.visualize_data)

    def visualize_data(self, compare_id=None):
        cow_id = self.cow_id_entry.get()
        data_type = self.data_type

        if not data_type:
            custom_error_messagebox("Error", "Please select a data type to visualize.", self.root)
            return

        if not cow_id:
            custom_error_messagebox("Error", "Please enter a Cow ID number.", self.root)
            return

        file_path = 'C:/Users/Jyothesh karnam/Desktop/Trail/TrailActivity.csv'  # Update this path as needed

        if data_type == "activity":
            plot_activity_levels(cow_id, compare_with_cow_id=compare_id, file_path=file_path)

    def center_window(self, width, height, x_offset=0):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2) + x_offset
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

def open_visualize_data(parent_frame):
    visualize_data_window = tk.Toplevel(parent_frame)
    app = VisualizeDataApp(visualize_data_window)
    visualize_data_window.transient(parent_frame)  # Set to be on top of the parent window
    visualize_data_window.grab_set()  # Modal-like behavior
    parent_frame.wait_window(visualize_data_window)  # Pause the main window until this one closes
