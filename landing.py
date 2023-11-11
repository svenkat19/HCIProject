import tkinter as tk
from tkinter import messagebox

def open_signup_form():
    signup_form = tk.Toplevel(root)
    window_width = 375
    window_height = 667
    signup_form.title("Signup Form")

    # Create and configure widgets for the signup form
    # You can add Entry widgets, labels, and other widgets as needed.

    # Example: Entry widget for username
    screen_width = signup_form.winfo_screenwidth()
    screen_height = signup_form.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2
    signup_form.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    username_label = tk.Label(signup_form, text="Username:")
    username_label.pack()

    username_entry = tk.Entry(signup_form)
    username_entry.pack()

    # Add other widgets for the signup form...

# Function to handle signup button click
def signup():
    #messagebox.showinfo("Signup", "Signup button clicked!")
    open_signup_form()

# Function to handle login button click
def login():
    
    messagebox.showinfo("Login", "Login button clicked!")

# Custom size for the window (adjust as needed)
window_width = 375
window_height = 667

# Create the main window
root = tk.Tk()
root.title("Smart Home")

# Set the window size and center it on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create and configure the title label
title_label = tk.Label(root, text="SMART HOME", font=("Helvetica", 14, "bold"), pady=10)
title_label.pack(fill="both", expand=True)

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(fill="both", expand=True)

# Create and configure the Signup button
signup_button = tk.Button(
    button_frame, text="Signup", command=signup, font=("Helvetica", 12), padx=20, pady=10,
    bg="black", fg="white"
)
signup_button.pack(side="top", pady=10)

# Create and configure the Login button
login_button = tk.Button(
    button_frame, text="Login", command=login, font=("Helvetica", 12), padx=20, pady=10,
    bg="black", fg="white"
)
login_button.pack(side="top", pady=10)

# Run the main loop
root.mainloop()
