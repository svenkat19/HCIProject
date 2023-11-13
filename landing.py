import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector
from datetime import datetime
import cv2
from PIL import Image, ImageTk

# Connect to the MySQL database (replace with your database details)
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="voter"
)

# Global variables
username_entry, phone_entry, selected_date_var, password_entry = None, None, None, None
login_username_entry = None

def open_signup_form():
    global username_entry, phone_entry, selected_date_var, password_entry

    # Hide the main window
    root.withdraw()
    
    # Create the signup form
    signup_form = tk.Toplevel(root)
    signup_form.title("Signup Form")

    # Set dimensions for the signup form
    window_width, window_height = 375, 667
    screen_width, screen_height = signup_form.winfo_screenwidth(), signup_form.winfo_screenheight()
    x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
    signup_form.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Elements for the signup form
    signup_heading = tk.Label(signup_form, text="SIGNUP", font=("Helvetica", 18, "bold"), pady=10)
    signup_heading.pack()

    username_label = tk.Label(signup_form, text="Username:", font=("Helvetica", 14))
    username_label.pack(pady=5)

    username_entry = tk.Entry(signup_form, font=("Helvetica", 14))
    username_entry.pack(pady=5)

    phone_label = tk.Label(signup_form, text="Phone Number:", font=("Helvetica", 14))
    phone_label.pack(pady=5)

    phone_entry = tk.Entry(signup_form, font=("Helvetica", 14))
    phone_entry.pack(pady=5)

    # Additional widgets
    additional_widgets_frame = tk.Frame(signup_form)
    global selected_date_var
    selected_date_var = tk.StringVar()
    selected_date_entry = tk.Entry(additional_widgets_frame, textvariable=selected_date_var,
                                   state='readonly', font=("Helvetica", 14), width=11)
    open_calendar_button = tk.Button(additional_widgets_frame, text="Calendar",
                                     command=lambda: open_calendar(selected_date_var),
                                     font=("Helvetica", 12), padx=5, pady=5, bg="black", fg="white")

    # Layout for additional widgets
    additional_widgets_frame.pack(padx=10, pady=5)
    selected_date_entry.grid(row=0, column=0, padx=(0, 10))
    open_calendar_button.grid(row=0, column=1)

    dob_label = tk.Label(signup_form, text="Date of Birth:", font=("Helvetica", 14))
    dob_label.pack(pady=5)

    password_label = tk.Label(signup_form, text="Admin Password:", font=("Helvetica", 14))
    password_label.pack(pady=5)

    password_entry = tk.Entry(signup_form, show="*", font=("Helvetica", 14))
    password_entry.pack(pady=5)

    proceed_button = tk.Button(signup_form, text="Proceed", command=lambda: proceed_signup(signup_form, username_entry.get(), selected_date_var.get(), phone_entry.get(), password_entry.get()),
                               font=("Helvetica", 12), padx=10, pady=5, bg="green", fg="white")
    proceed_button.pack(pady=10)

    back_button = tk.Button(signup_form, text="Back", command=lambda: show_root(signup_form),
                            font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
    back_button.place(x=10, y=10)  # Place the "Back" button in the top-left corner

    signup_form.protocol("WM_DELETE_WINDOW", lambda: show_root(signup_form))
def proceed_signup(signup_form, username, dob_str, phone_number, admin_password):
    # Check if the admin password is correct
    if admin_password != "admin1234":
        messagebox.showerror("Failure", "Incorrect admin password.")
        return

    # Convert the date string to the 'YYYY-MM-DD' format
    try:
        dob = datetime.strptime(dob_str, '%m/%d/%y').strftime('%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Failure", "Invalid date format. Please use MM/DD/YY.")
        return

    # Check if the username already exists in the database
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Username already exists, show failure dialog box
        messagebox.showerror("Failure", "Username already exists.")
        signup_form.lift()  # Bring the signup form to the front
    else:
        # Username doesn't exist, add user details to the database
        cursor.execute("INSERT INTO users (username, dob, phone_number) VALUES (%s, %s, %s)",
                       (username, dob, phone_number))
        db_connection.commit()

        # Clear the form
        clear_signup_form(signup_form)

        # Open the camera preview tab
        open_camera_preview(username)

def clear_signup_form(signup_form):
    # Clear the form fields
    username_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    selected_date_var.set("")  # Clear the date
    password_entry.delete(0, tk.END)

def show_root(signup_form):
    signup_form.destroy()
    root.deiconify()

def open_calendar(selected_date_var):
    calendar_window = tk.Toplevel(root)
    calendar_window.title("Calendar")

    def on_date_selected():
        selected_date_var.set("" + calendar.get_date())

    calendar = Calendar(calendar_window, selectmode="day", year=2000, month=1, day=1, font=("Helvetica", 14))
    calendar.pack(padx=10, pady=5)

    select_button = tk.Button(calendar_window, text="Select", command=on_date_selected,
                              font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
    select_button.pack(pady=10)

def open_camera_preview(username):
    camera_preview = tk.Toplevel(root)
    camera_preview.title("Camera Preview")

    # Open the camera
    cap = cv2.VideoCapture(0)

    def capture_image():
        ret, frame = cap.read()
        if ret:
            image_name = f"userimages/{username}.png"
            cv2.imwrite(image_name, frame)
            close_camera(cap, camera_preview)

            # Display a popup saying "Successfully registered user"
            messagebox.showinfo("Success", "Successfully registered user")

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img = ImageTk.PhotoImage(img.convert('RGBA'))
            label.config(image=img)
            label.image = img
            camera_preview.after(10, update_frame)

    label = tk.Label(camera_preview)
    label.pack()

    capture_button = tk.Button(camera_preview, text="Capture Image", command=capture_image,
                               font=("Helvetica", 12), padx=10, pady=5, bg="green", fg="white")
    capture_button.pack(pady=10)

    update_frame()

    camera_preview.protocol("WM_DELETE_WINDOW", lambda: close_camera(cap, camera_preview))

def close_camera(cap, camera_preview):
    cap.release()
    camera_preview.destroy()

# ...

def open_login_page():
    # Hide the main window
    root.withdraw()

    # Create the login page
    login_page = tk.Toplevel(root)
    login_page.title("Login")

    # Set dimensions for the login page
    window_width, window_height = 375, 667
    screen_width, screen_height = login_page.winfo_screenwidth(), login_page.winfo_screenheight()
    x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
    login_page.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Elements for the login page
    login_heading = tk.Label(login_page, text="LOGIN", font=("Helvetica", 18, "bold"), pady=30)
    login_heading.pack()

    global login_username_entry
    login_username_label = tk.Label(login_page, text="Enter your Username:", font=("Helvetica", 14))
    login_username_label.pack(pady=50)

    global login_username_entry
    login_username_entry = tk.Entry(login_page, font=("Helvetica", 14))
    login_username_entry.pack(pady=20, ipady=3)  # Increase the internal padding (ipady) for vertical centering

    proceed_button = tk.Button(login_page, text="Proceed", command=lambda: proceed_login(login_page),
                               font=("Helvetica", 12), padx=10, pady=5, bg="green", fg="white")
    proceed_button.pack(pady=10)

    # Back button
    back_button = tk.Button(login_page, text="Back", command=lambda: show_root(login_page),
                            font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
    back_button.place(x=10, y=10)  # Place the "Back" button in the top-left corner

    login_page.protocol("WM_DELETE_WINDOW", lambda: show_root(login_page))

# ...


def proceed_login(login_page):
    # You can add login functionality here based on the entered username
    username = login_username_entry.get()

    # Check if the username exists in the database
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Username found, open a blank page or perform any other action
        open_blank_page(username)
    else:
        # Username not found, show a popup
        messagebox.showerror("Login Failure", "Username not found.")

def open_blank_page(username):
    blank_page = tk.Toplevel(root)
    blank_page.title("Blank Page")

    # Set dimensions for the blank page
    window_width, window_height = 375, 667
    screen_width, screen_height = blank_page.winfo_screenwidth(), blank_page.winfo_screenheight()
    x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
    blank_page.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    label = tk.Label(blank_page, text=f"Welcome, {username}!", font=("Helvetica", 14, "bold"), pady=30)
    label.pack(fill="both", expand=True)

    back_button = tk.Button(blank_page, text="Back", command=blank_page.destroy,
                            font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
    back_button.place(x=10, y=10)  # Place the "Back" button in the top-left corner

    blank_page.protocol("WM_DELETE_WINDOW", lambda: blank_page.destroy())

# Main window (landing page)
window_width, window_height = 375, 667
root = tk.Tk()
root.title("Smart Home")

screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

title_label = tk.Label(root, text="SMART HOME", font=("Helvetica", 14, "bold"), pady=10)
title_label.pack(fill="both", expand=True)

button_frame = tk.Frame(root)
button_frame.pack(fill="both", expand=True)

signup_button = tk.Button(
    button_frame, text="Signup", command=open_signup_form, font=("Helvetica", 12), padx=20, pady=10,
    bg="black", fg="white"
)
signup_button.pack(side="top", pady=10)

login_button = tk.Button(
    button_frame, text="Login", command=open_login_page,
    font=("Helvetica", 12), padx=20, pady=10, bg="black", fg="white"
)
login_button.pack(side="top", pady=10)

root.mainloop()

# Close the database connection when the application is closed
db_connection.close()
