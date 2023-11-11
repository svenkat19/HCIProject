import tkinter as tk
from tkinter import messagebox

def open_signup_form():
    global root
    root.withdraw()  # Hide the root window
    signup_form = tk.Toplevel(root)
    signup_form.title("Signup Form")

    window_width = 375
    window_height = 667

    # Calculate the position and size of the signup form
    screen_width = signup_form.winfo_screenwidth()
    screen_height = signup_form.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    signup_form.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    
    # Add a Back button in the top-left corner
    back_button = tk.Button(signup_form, text="Back", command=lambda: show_root(signup_form),
                            font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
    back_button.pack(anchor="nw", padx=10, pady=10)

    username_label = tk.Label(signup_form, text="Username:")
    username_label.pack()

    username_entry = tk.Entry(signup_form)
    username_entry.pack()

    # Add other widgets for the signup form...

    # Bind the closing event to a function that shows the root window
    signup_form.protocol("WM_DELETE_WINDOW", lambda: show_root(signup_form))

def show_root(signup_form):
    global root
    signup_form.destroy()  # Destroy the signup_form window
    root.deiconify()  # Show the root window

# Function to handle signup button click
def signup():
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
