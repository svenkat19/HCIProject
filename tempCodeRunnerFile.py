import tkinter as tk
from tkinter import messagebox

def signup():
    messagebox.showinfo("Signup", "Signup button clicked!")

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
title_label.pack(side="top", fill="both", expand=True)

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(side="top", fill="both", expand=True)

# Create and configure the Signup button
signup_button = tk.Button(button_frame, text="Signup", command=signup, font=("Helvetica", 12), padx=20, pady=10)
signup_button.pack(side="top", pady=10)

# Create and configure the Login button
login_button = tk.Button(button_frame, text="Login", command=login, font=("Helvetica", 12), padx=20, pady=10)
login_button.pack(side="top", pady=10)

# Run the main loop
root.mainloop()
