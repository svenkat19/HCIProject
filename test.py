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
        self.curUser = None  # Variable to store the current user

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
        # ... (unchanged)

    def open_signup_form(self):
        # ... (unchanged)

    def proceed_signup(self):
        # ... (unchanged)

        # Open the camera preview tab
        self.open_camera_preview(username)

    def clear_signup_form(self):
        # ... (unchanged)

    def show_root(self, signup_form):
        signup_form.destroy()
        self.root.deiconify()

    def open_calendar(self, selected_date_var):
        # ... (unchanged)

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

        # ... (unchanged)

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
            # Save the current user for later use
            self.curUser = username
            # Open the camera preview tab for login
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
        # ... (unchanged)

# Main application loop
if __name__ == "__main__":
    window = tk.Tk()
    app = VoterApp(window)
    window.mainloop()

    # Close the database connection when the application is closed
    app.db_connection.close()
