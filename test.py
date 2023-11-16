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

    # ... (rest of the code remains the same)

    def open_blank_page(self, username):
        blank_page = tk.Toplevel(self.root)
        blank_page.title("Blank Page")

        window_width, window_height = 375, 667
        screen_width, screen_height = blank_page.winfo_screenwidth(), blank_page.winfo_screenheight()
        x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        blank_page.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Load background image
        background_image_path = "D:\\VIT\\Fall_Semester_2023-24\\HCI\\HCIProject\\images\\home.jpg"
        background_image = Image.open(background_image_path)
        background_image = background_image.resize((window_width, window_height), Image.ANTIALIAS)
        background_photo = ImageTk.PhotoImage(background_image)

        # Set background image
        background_label = tk.Label(blank_page, image=background_photo)
        background_label.image = background_photo
        background_label.place(relwidth=1, relheight=1)

        # Logout button
        logout_button = tk.Button(blank_page, text="Logout", command=lambda: self.logout_and_open_landing_page(blank_page),
                                  font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
        logout_button.place(relx=0.85, rely=0.05)  # Place the "Logout" button at the top-right corner

        # Help button
        help_button = tk.Button(blank_page, text="Help", command=self.open_help_page,
                                font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
        help_button.place(relx=0.85, rely=0.12)  # Place the "Help" button below the "Logout" button

        blank_page.protocol("WM_DELETE_WINDOW", lambda: self.logout_and_open_landing_page(blank_page))

    def open_help_page(self):
        help_page = tk.Toplevel(self.root)
        help_page.title("Help Page")

        window_width, window_height = 375, 667
        screen_width, screen_height = help_page.winfo_screenwidth(), help_page.winfo_screenheight()
        x_position, y_position = (screen_width - window_width) // 2, (screen_height - window_height) // 2
        help_page.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Help content
        help_content = tk.Label(help_page, text="This is the help page.", font=("Helvetica", 14), pady=30)
        help_content.pack(fill="both", expand=True)

        # Back button
        back_button = tk.Button(help_page, text="Back", command=help_page.destroy,
                                font=("Helvetica", 12), padx=10, pady=5, bg="black", fg="white")
        back_button.place(x=10, y=10)  # Place the "Back" button in the top-left corner

        help_page.protocol("WM_DELETE_WINDOW", lambda: help_page.destroy())

    def logout_and_open_landing_page(self, page_to_close):
        page_to_close.destroy()
        self.show_root(self.root)

    # ... (rest of the code remains the same)

# Main application loop
if __name__ == "__main__":
    window = tk.Tk()
    app = VoterApp(window)
    window.mainloop()

    # Close the database connection when the application is closed
    app.db_connection.close()
