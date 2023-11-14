import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import mysql.connector
from datetime import datetime
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace

class VoterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Home")
        self.db_connection = self.connect_to_database()

        # Global variables
        self.username_entry, self.phone_entry, self.selected_date_var, self.password_entry = None, None, None, None
        self.login_username_entry = None

        # Main window (landing page)
        self.setup_main_window()

    def connect_to_database(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="voter"
        )

    def setup_main_window(self):
        window_width, window_height = 375, 667
        screen_width, screen_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        title_label = tk.Label(self.root, text="SMART HOME", font=("Helvetica", 14, "bold"), pady=10)
        title_label.pack(fill="both", expand=True)

        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="both", expand=True)

        signup_button = tk.Button(
            button_frame, text="Signup", command=self.open_signup_form, font=("Helvetica", 12), padx=20, pady=10,
            bg="black", fg="white"
        )
        signup_button.pack(side="top", pady=10)

        login_button = tk.Button(
            button_frame, text="Login", command=self.open_login_page,
            font=("Helvetica", 12), padx=20, pady=10, bg="black", fg="white"
        )
        login_button.pack(side="top", pady=10)

    def open_signup_form(self):
        self.root.withdraw()

        signup_form = tk.Toplevel(self.root)
        signup_form.title("Signup Form")

        window_width, window_height = 375, 667
        screen_width, screen_height = signup_form.winfo_screenwidth(), signup_form.winfo_screenheight()
        x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        signup_form.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Elements for the signup form
        signup_heading = tk.Label(signup_form, text="SIGNUP", font=("Helvetica", 18, "bold"), pady=10)
        signup_heading.pack()

        username_label = tk.Label(signup_form, text="Username:", font=("Helvetica", 14))
        username_label.pack(pady=5)

        self.username_entry = tk.Entry(signup_form, font=("Helvetica", 14))
        self.username_entry.pack(pady=5)

        phone_label = tk.Label(signup_form, text="Phone Number:", font=("Helvetica", 14))
        phone_label.pack(pady=5)

        self.phone_entry = tk.Entry(signup_form, font=("Helvetica", 14))
        self.phone_entry.pack(pady=5)

        additional_widgets_frame = tk.Frame(signup_form)
        self.selected_date_var = tk.StringVar()
        selected_date_entry = tk.Entry(additional_widgets_frame, textvariable=self.selected_date_var,
                                       state='readonly', font=("Helvetica", 14), width=11)
        open_calendar_button = tk.Button(additional_widgets_frame, text="Calendar",
                                         command=lambda: self.open_calendar(self.selected_date_var),
                                         font=("Helvetica", 12), padx=5, pady=5, bg="black", fg="white")

        # Layout for additional widgets
        additional_widgets_frame.pack(padx=10, pady=5)
        selected_date_entry.grid(row=0, column=0, padx=(0, 10))
        open_calendar_button.grid(row=0, column=1)

        dob_label = tk.Label(signup_form, text="Date of Birth:", font=("Helvetica", 14))
        dob_label.pack(pady=5)

        password_label = tk.Label(signup_form, text="Admin Password:", font=("Helvetica", 14))
        password_label.pack(pady=5)

        self.password_entry = tk.Entry(signup_form, show="*", font=("Helvetica", 14))
        self.password_entry.pack(pady=5)

        proceed_button = tk.Button(signup_form, text="Proceed", command=self.proceed_signup,
                                   font=("Helvetica", 12), padx=10, pady=5, bg="green", fg="white")
        proceed_button.pack(pady=10)

        back_button = tk.Button(signup_form, text="Back", command=lambda: self.show_root(signup_form),
                                font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
        back_button.place(x=10, y=10)  # Place the "Back" button in the top-left corner

        signup_form.protocol("WM_DELETE_WINDOW", lambda: self.show_root(signup_form))

    def proceed_signup(self):
        username = self.username_entry.get()
        dob_str = self.selected_date_var.get()
        phone_number = self.phone_entry.get()
        admin_password = self.password_entry.get()

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
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            # Username already exists, show failure dialog box
            messagebox.showerror("Failure", "Username already exists.")
            return
        else:
            # Username doesn't exist, add user details to the database
            cursor.execute("INSERT INTO users (username, dob, phone_number) VALUES (%s, %s, %s)",
                           (username, dob, phone_number))
            self.db_connection.commit()

            # Clear the form
            self.clear_signup_form()

            # Open the camera preview tab
            self.open_camera_preview(username)
        self.open_camera_preview(username)

    def clear_signup_form(self):
        # Clear the form fields
        self.username_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.selected_date_var.set("")  # Clear the date
        self.password_entry.delete(0, tk.END)

    def show_root(self, signup_form):
        signup_form.destroy()
        self.root.deiconify()

    def open_calendar(self, selected_date_var):
        calendar_window = tk.Toplevel(self.root)
        calendar_window.title("Calendar")

        def on_date_selected():
            selected_date_var.set("" + calendar.get_date())

        calendar = Calendar(calendar_window, selectmode="day", year=2000, month=1, day=1, font=("Helvetica", 14))
        calendar.pack(padx=10, pady=5)

        select_button = tk.Button(calendar_window, text="Select", command=on_date_selected,
                                  font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
        select_button.pack(pady=10)

    def open_camera_preview(self, username):
        camera_preview = tk.Toplevel(self.root)
        camera_preview.title("Camera Preview")

        # Open the camera
        cap = cv2.VideoCapture(0)

        def capture_image():
            ret, frame = cap.read()
            if ret:
                image_name = f"userimages/{username}.png"
                cv2.imwrite(image_name, frame)
                self.close_camera(cap, camera_preview)
                self.perform_face_verification(username, image_name)

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

        camera_preview.protocol("WM_DELETE_WINDOW", lambda: self.close_camera(cap, camera_preview))

    def close_camera(self, cap, camera_preview):
        cap.release()
        camera_preview.destroy()

    def perform_face_verification(self, username, captured_image_path):
        try:
            user_image_path = f"userimages/{username}.png"
            result = DeepFace.verify(user_image_path, captured_image_path)

            if result["verified"]:
                messagebox.showinfo("Success", "Successfully registered user")
            else:
                messagebox.showerror("Failure", "Face scan failed. Please try again.")
        except Exception as e:
            print("Error during face verification:", str(e))

    def open_login_page(self):
        self.root.withdraw()

        login_page = tk.Toplevel(self.root)
        login_page.title("Login")

        window_width, window_height = 375, 667
        screen_width, screen_height = login_page.winfo_screenwidth(), login_page.winfo_screenheight()
        x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        login_page.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Elements for the login page
        login_heading = tk.Label(login_page, text="LOGIN", font=("Helvetica", 18, "bold"), pady=30)
        login_heading.pack()

        self.login_username_entry = tk.Entry(login_page, font=("Helvetica", 14))
        self.login_username_entry.pack(pady=20, ipady=3)  # Increase the internal padding (ipady) for vertical centering

        proceed_button = tk.Button(login_page, text="Proceed", command=self.proceed_login,
                                   font=("Helvetica", 12), padx=10, pady=5, bg="green", fg="white")
        proceed_button.pack(pady=10)

        # Back button
        back_button = tk.Button(login_page, text="Back", command=lambda: self.show_root(login_page),
                                font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
        back_button.place(x=10, y=10)  # Place the "Back" button in the top-left corner

        login_page.protocol("WM_DELETE_WINDOW", lambda: self.show_root(login_page))

    def proceed_login(self):
        username = self.login_username_entry.get()

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            self.curUser = username  # Set curUser when login is successful
            self.open_blank_page(username)
            self.open_camera_preview_for_login()
        else:
            messagebox.showerror("Login Failure", "Username not found.")
    def open_camera_preview_for_login(self):
        camera_preview = tk.Toplevel(self.root)
        camera_preview.title("Camera Preview - Login")

        # Open the camera
        cap = cv2.VideoCapture(0)

        def capture_image():
            ret, frame = cap.read()
            if ret:
                image_name = f"captured/{self.curUser}_login.png"
                cv2.imwrite(image_name, frame)
                self.close_camera(cap, camera_preview)
                self.perform_face_verification_for_login(self.curUser, image_name)

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

        camera_preview.protocol("WM_DELETE_WINDOW", lambda: self.close_camera(cap, camera_preview))

    def perform_face_verification_for_login(self, username, captured_image_path):
        try:
            user_image_path = f"userimages/{username}.png"
            result = DeepFace.verify(user_image_path, captured_image_path)

            if result["verified"]:
                messagebox.showinfo("Login Success", "Successfully logged in")
            else:
                messagebox.showerror("Login Failure", "Face scan failed. Please try again.")
        except Exception as e:
            print("Error during face verification:", str(e))
    def open_blank_page(self, username):
        blank_page = tk.Toplevel(self.root)
        blank_page.title("Blank Page")

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

# Main application loop
if __name__ == "__main__":
    window = tk.Tk()
    app = VoterApp(window)
    window.mainloop()

    # Close the database connection when the application is closed
    app.db_connection.close()
