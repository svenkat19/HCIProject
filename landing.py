import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar

def open_signup_form():
    global root
    root.withdraw()
    signup_form = tk.Toplevel(root)
    signup_form.title("Signup Form")

    window_width = 600  # Adjusted width for additional widgets
    window_height = 667

    screen_width = signup_form.winfo_screenwidth()
    screen_height = signup_form.winfo_screenheight()
    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    signup_form.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    back_button = tk.Button(signup_form, text="Back", command=lambda: show_root(signup_form),
                            font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
    back_button.pack(anchor="nw", padx=10, pady=10)

    username_label = tk.Label(signup_form, text="Username:", font=("Helvetica", 14))
    username_label.pack()

    username_entry = tk.Entry(signup_form, font=("Helvetica", 14))
    username_entry.pack()

    phone_label = tk.Label(signup_form, text="Phone Number:", font=("Helvetica", 14))
    phone_label.pack()

    phone_entry = tk.Entry(signup_form, font=("Helvetica", 14))
    phone_entry.pack()

    dob_label = tk.Label(signup_form, text="Date of Birth:", font=("Helvetica", 14))
    dob_label.pack()

    # Additional widgets
    additional_widgets_frame = tk.Frame(signup_form)
    additional_widgets_frame.pack(padx=10, pady=5)

    # Text box to display selected date
    selected_date_var = tk.StringVar()
    selected_date_entry = tk.Entry(additional_widgets_frame, textvariable=selected_date_var, state='readonly',
                                   font=("Helvetica", 14))
    selected_date_entry.grid(row=0, column=0, padx=(0, 10))

    # Button to open the calendar
    open_calendar_button = tk.Button(additional_widgets_frame, text="Calendar",
                                     command=lambda: open_calendar(selected_date_var),
                                     font=("Helvetica", 12), padx=5, pady=5, bg="black", fg="white")
    open_calendar_button.grid(row=0, column=1)

    password_label = tk.Label(signup_form, text="Admin Password:", font=("Helvetica", 14))
    password_label.pack()

    password_entry = tk.Entry(signup_form, show="*", font=("Helvetica", 14))
    password_entry.pack()

    signup_form.protocol("WM_DELETE_WINDOW", lambda: show_root(signup_form))

def show_root(signup_form):
    global root
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

def signup():
    open_signup_form()

def login():
    messagebox.showinfo("Login", "Login button clicked!")

window_width = 375
window_height = 667

root = tk.Tk()
root.title("Smart Home")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

title_label = tk.Label(root, text="SMART HOME", font=("Helvetica", 14, "bold"), pady=10)
title_label.pack(fill="both", expand=True)

button_frame = tk.Frame(root)
button_frame.pack(fill="both", expand=True)

signup_button = tk.Button(
    button_frame, text="Signup", command=signup, font=("Helvetica", 12), padx=20, pady=10,
    bg="black", fg="white"
)
signup_button.pack(side="top", pady=10)

login_button = tk.Button(
    button_frame, text="Login", command=login, font=("Helvetica", 12), padx=20, pady=10,
    bg="black", fg="white"
)
login_button.pack(side="top", pady=10)

root.mainloop()
