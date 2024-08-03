# utils.py
import tkinter as tk

def custom_error_messagebox(title, message, parent):
    custom_box = tk.Toplevel(parent)
    custom_box.title(title)
    custom_box.configure(bg='black')

    message_label = tk.Label(custom_box, text=message, bg='black', fg='white', font=('Helvetica', 11))
    message_label.pack(padx=40, pady=(40, 10))

    continue_button = tk.Button(custom_box, text="Continue", command=custom_box.destroy, bg='#2e8b57', fg='white', font=('Helvetica', 11, 'bold'), width=10, height=2, bd=0, highlightthickness=0)
    continue_button.pack(pady=(10, 20))

    custom_box.transient(parent)
    custom_box.grab_set()

    # Position the message box at the center of the parent window
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (custom_box.winfo_reqwidth() // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (custom_box.winfo_reqheight() // 2)
    custom_box.geometry(f'+{x}+{y}')

    parent.wait_window(custom_box)

def custom_visualize_messagebox(title, message, parent, callback=None):
    custom_box = tk.Toplevel(parent)
    custom_box.title(title)
    custom_box.configure(bg='black')

    message_label = tk.Label(custom_box, text=message, bg='black', fg='white', font=('Helvetica', 11))
    message_label.pack(padx=40, pady=(20, 10))

    compare_label = tk.Label(custom_box, text="Would you like to compare with another cow?", bg='black', fg='white', font=('Helvetica', 11))
    compare_label.pack(padx=40, pady=(10, 10))

    compare_frame = tk.Frame(custom_box, bg='black')
    compare_frame.pack(padx=40, pady=(10, 20))

    vcmd = (custom_box.register(validate_cow_id), '%P')
    
    compare_id_label = tk.Label(compare_frame, text="Cow ID Number:", bg='black', fg='white', font=('Helvetica', 11))
    compare_id_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
    
    compare_entry = tk.Entry(compare_frame, font=('Helvetica', 11), width=20, validate='key', validatecommand=vcmd)
    compare_entry.grid(row=0, column=1, padx=10, pady=10, ipady=5, sticky=tk.W)

    continue_button = tk.Button(custom_box, text="Continue", command=lambda: on_continue(custom_box, callback, compare_entry), bg='#2e8b57', fg='white', font=('Helvetica', 11, 'bold'), width=10, height=2, bd=0, highlightthickness=0)
    continue_button.pack(pady=(10, 20))

    custom_box.transient(parent)
    custom_box.grab_set()

    # Position the message box at the center of the parent window
    parent.update_idletasks()
    x = parent.winfo_x() + (parent.winfo_width() // 2) - (custom_box.winfo_reqwidth() // 2)
    y = parent.winfo_y() + (parent.winfo_height() // 2) - (custom_box.winfo_reqheight() // 2)
    custom_box.geometry(f'+{x}+{y}')

    parent.wait_window(custom_box)

def validate_cow_id(P):
    if P.isdigit() and len(P) <= 4:
        return True
    elif P == "":
        return True
    else:
        return False

def on_continue(custom_box, callback, compare_entry):
    compare_id = compare_entry.get()
    if compare_id and not validate_cow_id(compare_id):
        tk.messagebox.showerror("Error", "Please enter a valid 4-digit Cow ID number.")
    else:
        if callback:
            callback(compare_id)
        custom_box.destroy()
