import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox,ttk
import mysql.connector
from PIL import Image, ImageTk
import pandas as pd
import joblib
from datetime import datetime
from customtkinter import CTkImage
import matplotlib.pyplot as plt
from io import BytesIO
from customtkinter import CTkImage
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import random
import subprocess
import threading
import os
import tempfile

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pooji",  # ✅ Replace with your actual MySQL password
        database="dementia_app"  # ✅ Replace with your actual DB name
    )

# ------------------ MySQL Config ------------------
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="",#username
            password="",#password of sql
            database="dementia_app"# database name
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", str(err))
        return None

def insert_user(name, email, username, password):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, username, password) 
                VALUES (%s, %s, %s, %s)
            """, (name, email, username, password))
            conn.commit()
            return True
    except mysql.connector.Error as err:
        messagebox.showerror("MySQL Error", str(err))
        return False
    finally:
        if conn:
            conn.close()

# ------------------ Main Application ------------------
class DementiaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Initial Diagnosis of Dementia")
        #self.attributes("-fullscreen", True)

        self.state('zoomed')  # Best for development/testing

        self.minsize(1000, 1000)
        
        # Configure grid layout (3x3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Load model and features
        self.model = joblib.load("dementia_model.pkl")
        self.feature_columns = joblib.load("model_features.pkl")
        
        # Create container frame
        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Initialize frames
        self.frames = {}

        '''for F in (MainPage, TitlePage, AbstractPage, AlgorithmPage, 
                 LoginPage, RegisterPage, MedicalTestsPage, ResultPage, HistoryPage):
            page = F(parent=self.container, controller=self)
            self.frames[F] = page
            page.grid(row=0, column=0, sticky="nsew")'''
        
        self.show_frame(MainPage)
        
        # Bind escape key to toggle fullscreen
        #self.bind("<Escape>", lambda e: self.attributes("-fullscreen", True))
        #self.bind("<F11>", lambda e: self.attributes("-fullscreen", True))
        self.fullscreen = True  # Add at the top of __init__

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.exit_fullscreen)
    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)

    def exit_fullscreen(self, event=None):
        self.fullscreen = False
        self.attributes("-fullscreen", False)

    def show_frame(self, page_class):
        if page_class not in self.frames:
            self.frames[page_class] = page_class(parent=self.container, controller=self)
            self.frames[page_class].grid(row=0, column=0, sticky="nsew")

        frame = self.frames[page_class]
        frame.tkraise()

        if hasattr(frame, "on_show"):
            frame.on_show()  # ⬅ Triggers field reset or actions


    def show_frame(self, page_class):
        """Creates and raises a frame dynamically to prevent flashing."""
        if page_class not in self.frames:
            self.frames[page_class] = page_class(parent=self.container, controller=self)
            self.frames[page_class].grid(row=0, column=0, sticky="nsew")

        frame = self.frames[page_class]
        frame.tkraise()

        if hasattr(frame, "on_show"):
            frame.on_show()

class BackgroundPage(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.after(100, self.set_background_image)

    def set_background_image(self):
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        bg_image = Image.open("images/bg_image.png")
        bg_ctk = ctk.CTkImage(light_image=bg_image, size=(screen_w, screen_h))
        self.bg_label = ctk.CTkLabel(self, image=bg_ctk, text="")
        self.bg_label.image = bg_ctk
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.bg_label.lower()  # ✨ This line does the magic
# ------------------ Main Page ------------------
class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        # Background will be loaded after the widget is ready
        self.after(100, self.set_background_image)

        # === Background Image ===
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        bg_image = Image.open("images/bg_image.png")  # replace with your actual image name
        bg_ctk = ctk.CTkImage(light_image=bg_image, size=(screen_w, screen_h))

        self.bg_label = ctk.CTkLabel(self, image=bg_ctk, text="")
        self.bg_label.image = bg_ctk  # Keep a reference
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # === Main content container ===
        self.container = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.container.pack(pady=40, padx=60, fill="both", expand=True)
        # === Header with logos and title side by side ===
        header_frame = ctk.CTkFrame(self.container, fg_color="white")
        header_frame.pack(pady=20, padx=20, fill="x")
                # === Logo/Image before Title ===
        logo_image = Image.open("images/logo.jpeg")  # Replace with your actual logo path
        logo_ctk = ctk.CTkImage(light_image=logo_image, size=(150, 150))  # Adjust size as needed

        ctk.CTkLabel(self.container, image=logo_ctk, text="").pack(pady=10)
                
        # === Project Title ===
        ctk.CTkLabel(self.container, 
                     text="Initial Diagnosis of Dementia using Machine Learning Approach",
                     font=("Times New Roman", 34, "bold"), wraplength=700, justify="center",
                     text_color="black").pack(pady=30)

        # === Bottom Navigation Buttons Frame ===
        button_frame = ctk.CTkFrame(self.container, fg_color="white")
        button_frame.pack(pady=20, side="bottom")

        proceed_btn = ctk.CTkButton(button_frame, text="Proceed", width=180, height=50,
                                    command=lambda: controller.show_frame(TitlePage))
        proceed_btn.pack(side="left", padx=20)

        exit_btn = ctk.CTkButton(button_frame, text="Exit", width=180, height=50, fg_color="#d9534f",
                                command=self.confirm_exit)
        exit_btn.pack(side="right", padx=20)

    def confirm_exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.winfo_toplevel().destroy()
            #self.controller.destroy()

    def set_background_image(self):
        try:
            bg_image = Image.open("images/bg_image.png")  # Replace with your image
            screen_w = self.winfo_width()
            screen_h = self.winfo_height()
            bg_ctk = ctk.CTkImage(light_image=bg_image, size=(screen_w, screen_h))
            self.bg_label = ctk.CTkLabel(self, image=bg_ctk, text="")
            self.bg_label.image = bg_ctk  # Prevent garbage collection
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()  # Push to back
        except Exception as e:
            print("Failed to load background image:", e)
            
# ------------------ Second Page ------------------
class TitlePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # === Background Image ===
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        bg_image = Image.open("images/second_page_image.jpg")  # adjust path
        bg_ctk = ctk.CTkImage(light_image=bg_image, size=(screen_w, screen_h))

        self.bg_label = ctk.CTkLabel(self, image=bg_ctk, text="")
        self.bg_label.image = bg_ctk
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # === Project Title at the Top (ensure it's on top of bg) ===
        self.title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                                        font=ctk.CTkFont(size=28, weight="bold"),
                                        text_color="black", bg_color="transparent")
        self.title_label.place(relx=0.5, rely=0.05, anchor="center")  # center top

        # === Buttons Frame on Right ===
        # === Buttons Positioned Right Center with Clean Look ===
        btn_container = ctk.CTkFrame(self, fg_color="transparent")  # transparent container
        btn_container.place(relx=0.78, rely=0.5, anchor="center")  # ⬅ moved left from 0.85 to 0.78

        btn_style = dict(
            width=260,
            height=50,
            font=ctk.CTkFont(size=16),
            corner_radius=20,
            bg_color="transparent",
            hover_color="#e2e2e2"
        )

        ctk.CTkButton(btn_container, text="📝  Abstract", **btn_style,
                    command=lambda: controller.show_frame(AbstractPage)).pack(pady=12)

        ctk.CTkButton(btn_container, text="⚙  Algorithm & Example", **btn_style,
                    command=lambda: controller.show_frame(AlgorithmPage)).pack(pady=12)

        ctk.CTkButton(btn_container, text="❓  How to Use", **btn_style,
                    command=lambda: controller.show_frame(UsagePage)).pack(pady=12)

        ctk.CTkButton(btn_container, text="🔐  Login", fg_color="#5cb85c", text_color="white", **btn_style,
                    command=lambda: controller.show_frame(LoginPage)).pack(pady=12)

        ctk.CTkButton(btn_container, text="🔙  Back", fg_color="#d9534f", text_color="white", **btn_style,
                    command=lambda: controller.show_frame(MainPage)).pack(pady=12)


# ------------------ Abstract Page ------------------
class AbstractPage(BackgroundPage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#f0f8ff")  # light bluish-gray

                # === Title at Top ===
        # === Project Title at the Top ===
        title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                                font=ctk.CTkFont(size=28, weight="bold"),
                                text_color="black", anchor="center")
        title_label.pack(pady=(20, 10))

        # Main container for layout
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)

        # Title label at the top
        

        # Load and display image in the middle of the frame
        try:
            self.abstract_img = Image.open("images/abstract_img.png").resize((1500, 650), Image.LANCZOS)  # Adjust size if needed
            self.abstract_img_tk = ImageTk.PhotoImage(self.abstract_img)
            self.img_label = ctk.CTkLabel(self.container, image=self.abstract_img_tk, text="")
        except:
            self.img_label = ctk.CTkLabel(self.container, text="[Image Placeholder]", 
                                          font=ctk.CTkFont(size=20, weight="bold"), text_color="gray")

        self.img_label.pack(expand=True, pady=20)  # Ensure it stays centered

        # Back button at the bottom
        self.back_btn = ctk.CTkButton(self, text="Back", width=150, fg_color="#d9534f",
                                      command=lambda: controller.show_frame(TitlePage))
        self.back_btn.pack(pady=10)

# ------------------ Algorithm Page ------------------
class AlgorithmPage(BackgroundPage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#f0f8ff")  # light bluish-gray
                # === Title at Top ===
        # === Project Title at the Top ===
        title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                                font=ctk.CTkFont(size=28, weight="bold"),
                                text_color="black", anchor="center")
        title_label.pack(pady=(20, 10))

        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)

        self.title_label = ctk.CTkLabel(self.container, text="Algorithm", 
                                        font=ctk.CTkFont(family="Courier", size=30, underline=True))
        self.title_label.pack(pady=10)

        content = (
            "Random Forest Algorithm\n\n"
            "The Random Forest algorithm is a powerful AI algorithm that uses many decision trees to make better predictions.\n"
            "By combining the results of multiple trees, it improves accuracy and reduces mistakes. It is used for handling large\n"
            "data and works well for early predictions. It can handle and analyze different types of patient data, like memory test\n"
            "scores, lifestyle, and medical history, to predict dementia risk.\n\n"
            "1: Data Collection\n"
            "2: Data Preprocessing\n"
            "3: Model Selection\n"
            "4: Model Training\n"
            "5: Model Optimization\n"
            "6: Model Evaluation\n"
            "7: Deployment"
        )

        self.textbox = ctk.CTkTextbox(self.container, width=1200, height=550, 
                                      font=ctk.CTkFont(size=24), wrap="word")
        self.textbox.insert("1.0", content)
        self.textbox.configure(state="disabled")
        self.textbox.pack(pady=10)

        # Bottom button container
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)

        # Back button (Navigates to TitlePage)
        self.back_btn = ctk.CTkButton(self.bottom_frame, text="Back", width=150, fg_color="#d9534f",
                                      command=lambda: controller.show_frame(TitlePage))
        self.back_btn.pack(side="left", padx=40)

        # Example button (Navigates to ExamplePage)
        self.example_btn = ctk.CTkButton(self.bottom_frame, text="Example", width=150, fg_color="#5bc0de",
                                         command=lambda: controller.show_frame(ExamplePage))
        self.example_btn.pack(side="right", padx=40)

#-----------example Page--------------------
class ExamplePage(BackgroundPage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color="#f0f8ff")  # light bluish-gray
        # === Project Title at the Top ===
        title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                                font=ctk.CTkFont(size=28, weight="bold"),
                                text_color="black", anchor="center")
        title_label.pack(pady=(20, 10))

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)

       # self.title_label = ctk.CTkLabel(self.container, text="Example", 
        #                                font=ctk.CTkFont(family="Courier", size=20, underline=True))
        #self.title_label.pack(pady=10)

        # Load Example Image
        try:
            self.example_img = Image.open("images/example_image.png").resize((1500, 700), Image.LANCZOS)  # Adjust size if needed
            self.example_img_tk = ImageTk.PhotoImage(self.example_img)
            self.img_label = ctk.CTkLabel(self.container, image=self.example_img_tk, text="")
        except:
            self.img_label = ctk.CTkLabel(self.container, text="[Image Placeholder]", 
                                          font=ctk.CTkFont(size=20, weight="bold"), text_color="gray")

        self.img_label.pack(expand=True, pady=20)

        # Back button to return to AlgorithmPage
        self.back_btn = ctk.CTkButton(self, text="Back", width=150, fg_color="#d9534f",
                                      command=lambda: controller.show_frame(TitlePage))
        self.back_btn.pack(pady=10)

#-------------How to use-----------------
class UsagePage(BackgroundPage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#f0f8ff")  # light bluish-gray

        # === Project Title at the Top ===
        title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                                font=ctk.CTkFont(size=28, weight="bold"),
                                text_color="black", anchor="center")
        title_label.pack(pady=(20, 10))

        # Main container for layout
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)

        # Title label at the top
        

        # Load and display image in the middle of the frame
        try:
            self.abstract_img = Image.open("images/usage_image.png").resize((1500, 650), Image.LANCZOS)  # Adjust size if needed
            self.abstract_img_tk = ImageTk.PhotoImage(self.abstract_img)
            self.img_label = ctk.CTkLabel(self.container, image=self.abstract_img_tk, text="")
        except:
            self.img_label = ctk.CTkLabel(self.container, text="[Image Placeholder]", 
                                          font=ctk.CTkFont(size=20, weight="bold"), text_color="gray")

        self.img_label.pack(expand=True, pady=20)  # Ensure it stays centered

        # Back button at the bottom
        self.back_btn = ctk.CTkButton(self, text="Back", width=150, fg_color="#d9534f",
                                      command=lambda: controller.show_frame(TitlePage))
        self.back_btn.pack(pady=10)
# ------------------ Login Page ------------------
class LoginPage(BackgroundPage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
                # === Title at Top ===
                # === Project Title at the Top ===
        title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                                font=ctk.CTkFont(size=28, weight="bold"),
                                text_color="black", anchor="center")
        title_label.pack(pady=(20, 10))


        # Main container (holds login frame & image side by side)
        # === Main Container (Side-by-Side) ===
        self.container = ctk.CTkFrame(self, fg_color="#d0e7f9")  # soft blue
        self.container.pack(fill="both", expand=True, padx=60, pady=40)

        # ------------------- LEFT: LOGIN FORM -------------------
        self.form_frame = ctk.CTkFrame(self.container, fg_color="white", corner_radius=25)
        self.form_frame.pack(side="left", expand=True, fill="both", padx=30, pady=20)

        title_label = ctk.CTkLabel(self.form_frame, text="Login", 
                                font=ctk.CTkFont(family="Times New Roman", size=36, weight="bold"))
        title_label.pack(pady=30)

        input_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        input_frame.pack(pady=20)
        label_font = ctk.CTkFont(family="Arial", size=18, weight="bold")  # You can adjust size here


        # Username field
        ctk.CTkLabel(input_frame, text="Username", anchor="w", font=label_font).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(input_frame, width=250)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        # Password field
        ctk.CTkLabel(input_frame, text="Password", anchor="w", font=label_font).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(input_frame, width=250, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Eye toggle
        self.eye_icon = ctk.CTkButton(input_frame, text="👁", width=40, height=30, 
                                    fg_color="#a7b85c", command=self.toggle_password)
        self.eye_icon.grid(row=1, column=2, padx=5, pady=10)

        # Login Button
        self.login_btn = ctk.CTkButton(self.form_frame, text="Login", width=150, height=40, fg_color="#5cb85c",
                                    font=ctk.CTkFont(size=16), command=self.check_login)
        self.login_btn.pack(pady=10)

        # Register Prompt
        ctk.CTkLabel(self.form_frame, text="New user?", font=ctk.CTkFont(size=14)).pack(pady=5)

        self.register_btn = ctk.CTkButton(self.form_frame, text="Register Here", width=150, fg_color="#3498db",
                                        font=ctk.CTkFont(size=16), command=lambda: controller.show_frame(RegisterPage))
        self.register_btn.pack(pady=10)

        self.forgot_password_btn = ctk.CTkButton(
        self.form_frame, 
        text="Forgot Password?", 
        fg_color="transparent", 
        text_color="blue", 
        hover=False, 
        font=ctk.CTkFont(size=14, underline=True),
        command=self.forgot_password_popup
    )
        self.forgot_password_btn.pack(pady=(5, 0))
        # ------------------- RIGHT: IMAGE + MESSAGE -------------------
        right_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        right_frame.pack(side="right", expand=True, fill="both", padx=30, pady=20)
        try:
            self.login_img = Image.open("images/login_image.png").resize((500, 500), Image.LANCZOS)
            self.login_img_tk = ImageTk.PhotoImage(self.login_img)
            img_label = ctk.CTkLabel(right_frame, image=self.login_img_tk, text="")
            img_label.pack(pady=20)
        except:
            img_label = ctk.CTkLabel(right_frame, text="[Image]", font=ctk.CTkFont(size=20), text_color="gray")
            img_label.pack(pady=20)
        # Welcome Text
        caption = ("Empowering early diagnosis of dementia\n"
                "through technology and compassionate care.")
        caption_label = ctk.CTkLabel(right_frame, text=caption, justify="center", wraplength=300,
                                    font=ctk.CTkFont(size=18, weight="normal"), text_color="black")
        caption_label.pack(pady=10)

                # === Bottom: Back Button ===
        self.back_btn = ctk.CTkButton(self, text="Back", width=150, fg_color="#d9534f",
                                      command=lambda: controller.show_frame(TitlePage))
        self.back_btn.pack(side="bottom", pady=10)

    def forgot_password_popup(self):
    
        popup = ctk.CTkToplevel(self)
        popup.title("Reset Password")
        popup.geometry("500x400")
        popup.grab_set()         # 👉 Makes the popup modal (disables other windows)
        popup.focus_force()      # 👉 Forces focus on popup
        popup.attributes('-topmost', True)  # 👉 Ensures it stays on top (optional

        ctk.CTkLabel(popup, text="Enter your registered email:", font=ctk.CTkFont(size=14)).pack(pady=10)
        email_entry = ctk.CTkEntry(popup, width=300)
        email_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="New Password:", font=ctk.CTkFont(size=14)).pack(pady=10)
        new_pass_entry = ctk.CTkEntry(popup, width=300, show="*")
        new_pass_entry.pack(pady=5)

        ctk.CTkLabel(popup, text="Confirm Password:", font=ctk.CTkFont(size=14)).pack(pady=10)
        confirm_pass_entry = ctk.CTkEntry(popup, width=300, show="*")
        confirm_pass_entry.pack(pady=5)

        def reset_password():
            email = email_entry.get().strip()
            new_pass = new_pass_entry.get().strip()
            confirm_pass = confirm_pass_entry.get().strip()

            if not email or not new_pass or not confirm_pass:
                messagebox.showwarning("Input Error", "All fields are required.")
                return
            if new_pass != confirm_pass:
                messagebox.showerror("Mismatch", "Passwords do not match.")
                return
            if len(new_pass) < 6:
                messagebox.showerror("Weak Password", "Password must be at least 6 characters.")
                return

            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
                result = cursor.fetchone()
                if result:
                    cursor.execute("UPDATE users SET password = %s WHERE email = %s", (new_pass, email))
                    conn.commit()
                    messagebox.showinfo("Success", "Password updated successfully!")
                    popup.destroy()
                else:
                    messagebox.showerror("Error", "Email not found.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                if conn:
                    conn.close()

        ctk.CTkButton(popup, text="Reset Password", command=reset_password).pack(pady=20)
    def toggle_password(self):
        """Toggle password visibility"""
        if self.password_entry.cget("show") == "*":
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="",#username
                password="",#password of sql
                database="dementia_app"# database name
            )

            if conn:
                cursor = conn.cursor()
                # ✅ Fetch all 4 fields directly
                cursor.execute("SELECT user_id, name, email, username FROM users WHERE username=%s AND password=%s", 
                            (username, password))
                result = cursor.fetchone()

                if result:
                    user_id, name, email, username = result
                    self.controller.current_user_id = user_id

                    # Record login history
                    cursor.execute("INSERT INTO login_history (user_id, ip_address) VALUES (%s, '127.0.0.1')", (user_id,))
                    conn.commit()

                    self.controller.show_frame(DashboardPage)
                    # Set user info on Dashboard
                    self.dashboard = self.controller.frames[DashboardPage]
                    self.dashboard.set_user_info(name, email, username)

                    # Clear login fields
                    self.username_entry.delete(0, 'end')
                    self.password_entry.delete(0, 'end')

                    #self.controller.show_frame(DashboardPage)

                else:
                    messagebox.showerror("Error", "Invalid username or password")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

        finally:
            if conn:
                conn.close()

    
# ------------------ Register Page ------------------
class RegisterPage(BackgroundPage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # === Background Image ===
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        bg_image = Image.open("images/background image.jpeg")  # use your actual image
        bg_ctk = ctk.CTkImage(light_image=bg_image, size=(screen_w, screen_h))
        self.bg_label = ctk.CTkLabel(self, image=bg_ctk, text="")
        self.bg_label.image = bg_ctk
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
                # === Project Title at the Top ===
        title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                                font=ctk.CTkFont(size=28, weight="bold"),
                                text_color="black", anchor="center")
        title_label.pack(pady=(20, 10))

        # === Centered FORM FRAME ===
        self.form_container = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.form_container.pack(pady=50, ipadx=50, ipady=30)

        # Title
        ctk.CTkLabel(self.form_container, text="🧠 Welcome!\nRegister to begin early dementia detection.",
                     font=ctk.CTkFont(size=16, weight="bold"), text_color="black",
                     justify="center", wraplength=400).pack(pady=15)

        # Entry fields
        form_inner = ctk.CTkFrame(self.form_container, fg_color="transparent")
        form_inner.pack(padx=10, pady=5)

        fields = ["Name", "Email", "Username", "Password", "Confirm Password"]
        self.entries = {}

        for field in fields:
            row = ctk.CTkFrame(form_inner, fg_color="transparent")
            row.pack(pady=5)
            label = ctk.CTkLabel(row, text=field, width=120, anchor="w", font=ctk.CTkFont(size=14))
            label.pack(side="left", padx=5)

            entry = ctk.CTkEntry(row, width=220, show="*" if "Password" in field else "")
            entry.pack(side="left", padx=5)
            self.entries[field] = entry

        # Register button
        ctk.CTkButton(self.form_container, text="Register", width=160, height=35, fg_color="#5cb85c",
                      font=ctk.CTkFont(size=15), command=self.register_user).pack(pady=15)

        # === BULLETS BELOW THE FORM ===
        bullets_frame = ctk.CTkFrame(self, fg_color="red")
        bullets_frame.pack(pady=10)

        bullets = [
            "✔ Easy, secure registration",
            "✔ ML-based dementia screening",
            "✔ Built for caregivers"
        ]
        for b in bullets:
            ctk.CTkLabel(bullets_frame, text=b, font=ctk.CTkFont(size=14), text_color="Yellow").pack(anchor="center")

        # === BACK BUTTON AT BOTTOM ===
        self.back_btn = ctk.CTkButton(self, text="Back", width=150, height=35, fg_color="#d9534f",
                                      command=lambda: controller.show_frame(LoginPage))
        self.back_btn.pack(side="bottom", pady=20)

    # === REGISTRATION LOGIC ===
    def register_user(self):
        data = {key: entry.get().strip() for key, entry in self.entries.items()}

        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        if data["Password"] != data["Confirm Password"]:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if len(data["Password"]) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters!")
            return

        if "@" not in data["Email"] or "." not in data["Email"]:
            messagebox.showerror("Error", "Please enter a valid email address!")
            return

        if insert_user(data["Name"], data["Email"], data["Username"], data["Password"]):
            for entry in self.entries.values():
                entry.delete(0, 'end')
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.controller.show_frame(LoginPage)

class DashboardPage(BackgroundPage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#b3e5fc")  # light blue engaging background

        # === Title ===
        ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                     font=ctk.CTkFont(size=28, weight="bold"),
                     text_color="black").pack(pady=(20, 10))

        # === Welcome Message ===
        self.welcome_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=22, weight="bold"))
        self.welcome_label.pack(pady=(5, 10))

        # === User Card (with image + details) ===
        self.user_card = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.user_card.pack(pady=10, padx=30)

        # === Square Frame with Icon ===
        self.icon_wrapper = ctk.CTkFrame(self.user_card, width=160, height=160, corner_radius=20, fg_color="#e0e0e0")
        self.icon_wrapper.pack(pady=20)

        user_img_path = "images/user_icon.webp"  # replace with your image path
        if os.path.exists(user_img_path):
            user_img = Image.open(user_img_path).resize((100, 100))
            self.user_icon = ctk.CTkImage(light_image=user_img, size=(100, 100))
            self.icon_label = ctk.CTkLabel(self.icon_wrapper, image=self.user_icon, text="")
        else:
            self.icon_label = ctk.CTkLabel(self.icon_wrapper, text="🧑", font=ctk.CTkFont(size=40))

        self.icon_label.place(relx=0.5, rely=0.5, anchor="center")

        # === Rectangle Frame for Details ===
        self.details_frame = ctk.CTkFrame(self.user_card, fg_color="#f8f8f8", corner_radius=10)
        self.details_frame.pack(padx=40, pady=(10, 20), fill="x")

        self.name_label = ctk.CTkLabel(self.details_frame, text="", font=ctk.CTkFont(size=18))
        self.email_label = ctk.CTkLabel(self.details_frame, text="", font=ctk.CTkFont(size=16))
        self.username_label = ctk.CTkLabel(self.details_frame, text="", font=ctk.CTkFont(size=16))

        self.name_label.pack(pady=(10, 4))
        self.email_label.pack(pady=4)
        self.username_label.pack(pady=(4, 10))

        # === Buttons ===
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=30)

        btn_style = dict(width=160, height=45, font=ctk.CTkFont(size=15, weight="bold"))

        ctk.CTkButton(btn_frame, text="Take Test", fg_color="#5cb85c", text_color="white",
                      command=lambda: controller.show_frame(MedicalTestsPage), **btn_style).grid(row=0, column=0, padx=20)

        ctk.CTkButton(btn_frame, text="Logout", fg_color="#d9534f", text_color="white",
                      command=self.logout_user, **btn_style).grid(row=0, column=1, padx=20)

        ctk.CTkButton(btn_frame, text="History", fg_color="#f0ad4e", text_color="black",
                      command=lambda: controller.show_frame(HistoryPage), **btn_style).grid(row=0, column=2, padx=20)

    def set_user_info(self, name, email, username):
        self.welcome_label.configure(text=f"Welcome, {username}!")
        self.name_label.configure(text=f"Name: {name}")
        self.email_label.configure(text=f"Email: {email}")
        self.username_label.configure(text=f"Username: {username}")

    def logout_user(self):
        self.controller.current_user_id = None
        self.controller.latest_prediction = None

        # ✅ Clear fields from MedicalTestsPage
        if MedicalTestsPage in self.controller.frames:
            self.controller.frames[MedicalTestsPage].reset_page()

        self.controller.show_frame(LoginPage)

    def reset_page(self):
        self.clear_fields()
        self.set_username("")  # clear welcome label

    def clear_fields(self):
        self.gender_var.set("Select")
        self.age_entry.delete(0, "end")
        self.mmse_entry.delete(0, "end")
        self.weight_entry.delete(0, "end")
        self.height_entry.delete(0, "end")
        self.smoking_var.set("Select")
        self.alcohol_var.set("Select")
        self.activity_var.set("Select")
        self.sleep_entry.delete(0, "end")

        
# ------------------ Medical Tests Page ------------------
class MedicalTestsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # === Project Title at the Top ===
        title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                                font=ctk.CTkFont(size=28, weight="bold"),
                                text_color="black", anchor="center")
        title_label.pack(pady=(20, 10))

        #self.after(100, self.set_background_image)

        # === Background Image ===
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()

        bg_image = Image.open("images/test_image.jpeg")  # replace with your actual image name
        bg_ctk = ctk.CTkImage(light_image=bg_image, size=(screen_w, screen_h))

        self.bg_label = ctk.CTkLabel(self, image=bg_ctk, text="")
        self.bg_label.image = bg_ctk  # Keep a reference
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        
       

        # === Main Form Frame Centered on Screen ===
        self.form_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")  # Full form centered
        self.welcome_label = ctk.CTkLabel(
            self.form_frame,
            text="Medical Tests",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="black"
        )
        self.welcome_label.pack(pady=(20, 10))
        # === Container inside that frame ===
        self.form_container = ctk.CTkFrame(self.form_frame, fg_color="#ffffff", corner_radius=10)
        self.form_container.pack(padx=20, pady=20)  # packed inside the centered parent
                # === Form Header ===
        # Add additional fields here...
        self.fields = {}
        self.username = ""
        
        # Gender
        ctk.CTkLabel(self.form_container, text="Gender:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.gender_var = ctk.StringVar(value="Select")
        self.gender_menu = ctk.CTkOptionMenu(self.form_container, 
                                       values=["Male", "Female"],
                                       variable=self.gender_var)
        self.gender_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Age
        ctk.CTkLabel(self.form_container, text="Age:").grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.age_var = tk.StringVar()
        self.age_var.trace_add("write", self.validate_age_input)
        self.age_entry = ctk.CTkEntry(self.form_container, textvariable=self.age_var)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        # MMSE Score
        ctk.CTkLabel(self.form_container, text="MMSE Test Score:").grid(row=2, column=0, padx=10, pady=10, sticky="n")

        self.mmse_entry = ctk.CTkEntry(self.form_container, width=150, state="disabled")  # ⛔️ disable manual input
        self.mmse_entry.grid(row=2, column=1, padx=5, pady=10, sticky="w")

        self.mmse_test_btn = ctk.CTkButton(self.form_container, text="Start Test", width=100,
                                        command=self.launch_mmse_test)
        self.mmse_test_btn.grid(row=2, column=2, padx=5, pady=10, sticky="w")

        # Weight
        ctk.CTkLabel(self.form_container, text="Weight (kg):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.weight_entry = ctk.CTkEntry(self.form_container)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Height
        ctk.CTkLabel(self.form_container, text="Height (cm):").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.height_entry = ctk.CTkEntry(self.form_container)
        self.height_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        # Smoking
        ctk.CTkLabel(self.form_container, text="Smoking:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.smoking_var = ctk.StringVar(value="Select")
        self.smoking_menu = ctk.CTkOptionMenu(self.form_container, 
                                        values=["Yes", "No"],
                                        variable=self.smoking_var)
        self.smoking_menu.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        
        # Alcohol
        ctk.CTkLabel(self.form_container, text="Alcohol Consumption:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.alcohol_var = ctk.StringVar(value="Select")
        self.alcohol_menu = ctk.CTkOptionMenu(self.form_container, 
                                        values=["Heavy","Moderate","Light", "No"],
                                        variable=self.alcohol_var)
        self.alcohol_menu.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        
        # Physical Activity
        ctk.CTkLabel(self.form_container, text="Physical Activity:").grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.activity_var = ctk.StringVar(value="Select")
        self.activity_menu = ctk.CTkOptionMenu(self.form_container, 
                                         values=["Sedentary", "Moderate", "Active"],
                                         variable=self.activity_var)
        self.activity_menu.grid(row=7, column=1, padx=10, pady=10, sticky="w")
        
        # Sleep Hours
        ctk.CTkLabel(self.form_container, text="Sleep Hours:").grid(row=8, column=0, padx=10, pady=10, sticky="e")
        self.sleep_entry = ctk.CTkEntry(self.form_container)
        self.sleep_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        # === Buttons Under Form ===
        self.button_panel = ctk.CTkFrame(self.form_container, fg_color="transparent")
        self.button_panel.grid(row=999, column=0, columnspan=3, pady=(20, 10))  # row 999 ensures it’s always at the bottom

        self.clear_button = ctk.CTkButton(self.button_panel, text="Clear", width=120, fg_color="#f0ad4e", command=self.clear_fields)
        self.clear_button.pack(side="left", padx=5)

        self.back_button = ctk.CTkButton(self.button_panel, text="Back", width=120, fg_color="#d9534f",
                                        command=lambda: self.controller.show_frame(DashboardPage))
        self.back_button.pack(side="left", padx=5)

        self.predict_button = ctk.CTkButton(self.button_panel, text="Predict", width=150, fg_color="#33d756",
                                            command=self.predict_dementia)
        self.predict_button.pack(side="left", padx=5)
  
    def validate_age_input(self, *args):
        value = self.age_var.get()

        if hasattr(self, 'age_validation_job'):
            self.after_cancel(self.age_validation_job)

        self.age_validation_job = self.after(2000, self.perform_age_check, value)

    def perform_age_check(self, value):
        if not value:
            return
        if not value.isdigit():
            self.age_var.set('')
            return
        age = int(value)
        if age < 50 or age > 120:
            messagebox.showwarning("Invalid Age", "Age must be between 50 and 120")
            self.age_var.set('')

    def set_background_image(self):
        try:
            bg_image = Image.open("images/bg_image.png")  # Replace with your image
            screen_w = self.winfo_width()
            screen_h = self.winfo_height()
            bg_ctk = ctk.CTkImage(light_image=bg_image, size=(screen_w, screen_h))
            self.bg_label = ctk.CTkLabel(self, image=bg_ctk, text="")
            self.bg_label.image = bg_ctk  # Prevent garbage collection
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()  # Push to back
        except Exception as e:
            print("Failed to load background image:", e)


    def reset_page(self):
        self.clear_fields()
        self.set_username("")  # clear welcome label

    def launch_mmse_test(self):
        def run_test_and_poll():
            subprocess.Popen(["python", "mmse_test_gui.py"])

            # Poll for score file
            temp_file_path = os.path.join(tempfile.gettempdir(), "mmse_score.txt")

            # Wait until the file is created
            while not os.path.exists(temp_file_path):
                self.after(500, lambda: None)  # Wait non-blocking
                #continue

            # Read the score and fill the entry
            with open(temp_file_path, "r") as f:
                score = f.read().strip()
                
            try:
                mmse_score = int(score)
            except ValueError:
                mmse_score = 0  # fallback if something went wrong


            self.mmse_entry.configure(state="normal")
            self.mmse_entry.delete(0, "end")
            self.mmse_entry.insert(0, score)
            self.mmse_entry.configure(state="disabled")

            # Optionally delete the temp file
            os.remove(temp_file_path)

        # Run in background to avoid freezing the UI
        threading.Thread(target=run_test_and_poll, daemon=True).start()

    
    def set_username(self, username):
        self.username = username
        self.welcome_label.configure(text=f"Welcome {username}! Please enter your medical details.")
        
    
    def clear_fields(self):
        self.gender_var.set("Select")
        self.age_entry.delete(0, "end")
        self.mmse_entry.delete(0, "end")
        self.weight_entry.delete(0, "end")
        self.height_entry.delete(0, "end")
        self.smoking_var.set("Select")
        self.alcohol_var.set("Select")
        self.activity_var.set("Select")
        self.sleep_entry.delete(0, "end")
    
    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  # Convert cm to m
            bmi = weight / (height ** 2)
            return round(bmi, 2)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height")
            return None
    
    def submit_data(self):
        # Validate all fields
        if (self.gender_var.get() == "Select" or 
            self.smoking_var.get() == "Select" or 
            self.alcohol_var.get() == "Select" or 
            self.activity_var.get() == "Select"):
            messagebox.showerror("Error", "Please select all dropdown options")
            return
            
        try:
            age = int(self.age_entry.get())
            mmse_score = int(self.mmse_entry.get())
            sleep_hours = float(self.sleep_entry.get())
            bmi = self.calculate_bmi()
            
            if bmi is None:
                return
                
            # Save to database
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Check if patient already exists
                cursor.execute("SELECT patient_id FROM patients WHERE user_id=%s", 
                             (self.controller.current_user_id,))
                patient = cursor.fetchone()
                
                if patient:
                    # Update existing patient
                    cursor.execute("""
                        UPDATE patients 
                        SET gender=%s, age=%s,  bmi=%s,
                            smoking=%s, alcohol=%s, physical_activity=%s, sleep_hours=%s, mmse_score=%s
                        WHERE user_id=%s
                    """, (
                        self.gender_var.get(), age,
                        self.calculate_bmi(), self.smoking_var.get(),
                        self.alcohol_var.get(), self.activity_var.get(), sleep_hours, mmse_score,
                        self.controller.current_user_id
                    ))
                else:
                    # Insert new patient
                    cursor.execute("""
                        INSERT INTO patients 
                        (user_id, gender, age, bmi, smoking, alcohol, 
                         physical_activity, sleep_hours, mmse_score)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        self.controller.current_user_id, self.gender_var.get(), age, 
                        self.calculate_bmi(),
                        self.smoking_var.get(), self.alcohol_var.get(), self.activity_var.get(),
                        sleep_hours, mmse_score
                    ))
                
                conn.commit()
                messagebox.showinfo("Success", "Medical data saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                conn.close()

            
    def validate_numeric_input(self, value, field_name, allow_float=False):
        """Helper method to validate numeric inputs"""
        value = str(value).strip()  # Convert to string and remove whitespace
        if not value:
            messagebox.showerror("Error", f"{field_name} cannot be empty")
            return None
        
        try:
            return float(value) if allow_float else int(value)
        except ValueError:
            messagebox.showerror("Error", f"Please enter a valid number for {field_name}")
            return None
    
    def get_user_inputs(self):
        try:
            if (self.gender_var.get() == "Select" or 
                self.smoking_var.get() == "Select" or 
                self.alcohol_var.get() == "Select" or 
                self.activity_var.get() == "Select"):
                messagebox.showerror("Error", "Please select all dropdown options")
                return None

            # Numeric inputs
            age = int(self.age_entry.get())
            mmse_score = int(self.mmse_entry.get())
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = weight / ((height/100) ** 2)
            sleep_hours = float(self.sleep_entry.get())

            # Map categorical inputs to numbers
            gender = 1 if self.gender_var.get() == "Male" else 0
            smoking = 1 if self.smoking_var.get() == "Yes" else 0
            alcohol = {"No": 0, "Light": 1, "Moderate": 2,"Heavy": 3}[self.alcohol_var.get()]
            activity = {"Sedentary": 0, "Moderate": 1, "Active": 2}[self.activity_var.get()]

            return pd.DataFrame([{
                "Gender": gender,
                "Age": age,
                "MMSE Test": mmse_score,
                "BMI": round(bmi, 2),
                "Smoking": smoking,
                "Alcohol Consumption": alcohol,
                "Physical Activity": activity,
                "Sleep Hours": sleep_hours,
            }])

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            return None

    
    def predict_dementia(self):
        print("🧠 Predict button clicked")
        
        self.submit_data()  # Save data to DB

        user_data = self.get_user_inputs()
        print("📦 Data for prediction:", user_data)

        if user_data is None:
            print("❌ No user data collected.")
            return
        
        # 🧠 Extract necessary variables for history insert
        age = int(self.age_entry.get())
        mmse_score = int(self.mmse_entry.get())
        sleep_hours = float(self.sleep_entry.get())
        bmi = self.calculate_bmi()  # This already handles the math

        try:
            user_data = self.get_user_inputs()
            if user_data is None:
                return

            # 🎯 Run prediction
            prediction = self.controller.model.predict(user_data)[0]
            confidence = self.controller.model.predict_proba(user_data)[0].max() * 100
            risk_score = int(confidence)

            # 🔍 Extract fields for storing
            age = int(self.age_entry.get())
            mmse_score = int(self.mmse_entry.get())
            sleep_hours = float(self.sleep_entry.get())
            bmi = self.calculate_bmi()

            # 🔄 Store in database
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT patient_id FROM patients WHERE user_id=%s", 
                        (self.controller.current_user_id,))
            result = cursor.fetchone()

            if result:
                patient_id = result[0]
                cursor.execute("""
                    INSERT INTO medical_history (
                        patient_id, diagnosis, age, bmi, mmse_score, sleep_hours,
                        smoking, alcohol, physical_activity, gender
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    patient_id, prediction, age, bmi, mmse_score, sleep_hours,
                    self.smoking_var.get(), self.alcohol_var.get(),
                    self.activity_var.get(), self.gender_var.get()
                ))
                conn.commit()
                conn.close()
            else:
                messagebox.showerror("Error", "Patient record not found.")
                return

            # 📊 Show on Result Page
            user_info = {
                "Name": self.username,
                "Age": age,
                "Gender": self.gender_var.get(),
                "MMSE": mmse_score,
                "BMI": bmi,
                "Smoking": self.smoking_var.get(),
                "Alcohol Consumption": self.alcohol_var.get(),
                "Physical Activity": self.activity_var.get(),
                "Sleep Hours": sleep_hours
            }

            interpretation = self.get_interpretation(prediction, mmse_score, age)
            recommendation = ""  # ResultPage builds it

            self.controller.show_frame(ResultPage)
            result_page = self.controller.frames[ResultPage]
            result_page.show_result(
                user_info, prediction, confidence, risk_score,
                interpretation, recommendation
            )

        except Exception as e:
            print("🔥 Error during prediction:", e)
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")

        

    def get_interpretation(self, prediction, mmse_score, age):
        mmse_score = int(mmse_score)
        age = int(age)

        if prediction == "Dementia detected":
            base = "Severe cognitive impairment likely."
            if mmse_score < 20:
                base += " MMSE score indicates significant decline."
            if age > 65:
                base += " Advanced age increases vulnerability."
            return base

        elif prediction == "Mild Dementia":
            base = "Mild cognitive changes observed."
            if 21 <= mmse_score <= 26:
                base += " MMSE score supports early-stage symptoms."
            if age > 60:
                base += " Age-related factors may contribute."
            return base

        else:
            base = "Cognitive function appears stable."
            if mmse_score >= 27:
                base += " MMSE score is within normal limits."
            return base

# ------------------ Result Page ------------------
class ResultPage(BackgroundPage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # === Project Title at the Top ===
        title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                           font=ctk.CTkFont(size=28, weight="bold"),
                           text_color="black", anchor="center")
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="n")


        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        font_heading = ctk.CTkFont(size=20, weight="bold")
        font_label = ctk.CTkFont(size=18)
        self.content = ctk.CTkFrame(self)
        self.content.grid(row=0, column=0, columnspan=2, sticky="nsew")  # ✅ use grid consistently
        # === USER DETAILS ===
        self.user_card = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.user_card.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.user_card, text="User Details", font=ctk.CTkFont(size=18, weight="bold")).grid(row=0, column=0, columnspan=2, pady=(10, 5), padx=10, sticky="w")

        # Define user labels and placeholder values
        user_fields = ["Age", "Gender", "MMSE", "BMI", "Smoking", "Alcohol", "Activity", "Sleep Hours"]
        self.user_labels = {}

        for i, field in enumerate(user_fields, start=1):
            # Label (left column)
            ctk.CTkLabel(self.user_card, text=f"{field}:", font=ctk.CTkFont(size=14, weight="bold"), text_color="gray")\
                .grid(row=i, column=0, sticky="e", padx=(10, 5), pady=4)

            # Value (right column - to be updated later)
            label = ctk.CTkLabel(self.user_card, text="-", font=ctk.CTkFont(size=14), text_color="black")
            label.grid(row=i, column=1, sticky="w", padx=(5, 10), pady=4)
            self.user_labels[field] = label  # Store for later access

        # === PREDICTION SUMMARY ===
        self.summary_card = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.summary_card.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.summary_card, text="Prediction Summary", font=font_heading).grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=5)
        self.prediction_label = ctk.CTkLabel(self.summary_card, text="", font=font_label)
        self.risk_score_label = ctk.CTkLabel(self.summary_card, text="", font=font_label)
        self.confidence_label = ctk.CTkLabel(self.summary_card, text="", font=font_label)
        self.mmse_label = ctk.CTkLabel(self.summary_card, text="", font=font_label)
        self.bmi_label = ctk.CTkLabel(self.summary_card, text="", font=font_label)
        self.model_accuracy_label = ctk.CTkLabel(self.summary_card, text="Model Accuracy: 87.00%", font=font_label)
        for i, lbl in enumerate([
            self.prediction_label,
            self.risk_score_label,
            self.confidence_label,
            self.mmse_label,
            self.bmi_label,
            self.model_accuracy_label
        ], start=1):
            lbl.grid(row=i, column=0, sticky="w", padx=10, pady=2)
            
        # === INTERPRETATION & RECOMMENDATION ===
        self.interpret_card = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.interpret_card.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(self.interpret_card, text="Interpretation", font=font_heading).grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        self.interpretation_label = ctk.CTkLabel(self.interpret_card, text="", font=font_label, wraplength=300, justify="left")
        self.interpretation_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        ctk.CTkLabel(self.interpret_card, text="Recommendation", font=font_heading).grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.recommendation_label = ctk.CTkLabel(self.interpret_card, text="", font=font_label, wraplength=300, justify="left")
        self.recommendation_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        # === PIE CHART ===
        self.chart_card = ctk.CTkFrame(self, fg_color="white", corner_radius=15)
        self.chart_card.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        self.chart_label = ctk.CTkLabel(self.chart_card, text="")
        self.chart_label.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # === BUTTON ROW ===
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.back_btn = ctk.CTkButton(self.button_frame, text="Back",fg_color="#422ec3", hover_color="#422ec3", command=lambda: controller.show_frame(DashboardPage))
        self.export_btn = ctk.CTkButton(self.button_frame, text="Export PDF",fg_color="#5bc0de", hover_color="#31b0d5", command=self.export_pdf)
        self.history_btn = ctk.CTkButton(self.button_frame, text="View History",fg_color="#c8316d", hover_color="#c8316d", command=lambda: controller.show_frame(HistoryPage))
        self.logout_btn = ctk.CTkButton(self.button_frame, text="Logout", fg_color="#dc3e22", hover_color="#dc3e22",command=self.logout_user)

        self.back_btn.grid(row=0, column=0, padx=20)
        self.export_btn.grid(row=0, column=1, padx=20)
        self.history_btn.grid(row=0, column=2, padx=20)
        self.logout_btn.grid(row=0, column=3, padx=10)

    def logout_user(self):
        self.controller.current_user_id = None
        self.controller.latest_prediction = None
        self.controller.show_frame(LoginPage)

    def show_result(self, user_info, prediction, confidence, risk_score, interpretation, recommendation):
        # Update structured user detail labels
        #self.user_labels["Name"].configure(text=user_info.get("Name", "-"))
        self.user_labels["Age"].configure(text=user_info.get("Age", "-"))
        self.user_labels["Gender"].configure(text=user_info.get("Gender", "-"))
        self.user_labels["MMSE"].configure(text=user_info.get("MMSE", "-"))
        self.user_labels["BMI"].configure(text=user_info.get("BMI", "-"))
        self.user_labels["Smoking"].configure(text=user_info.get("Smoking", "-"))
        self.user_labels["Alcohol"].configure(text=user_info.get("Alcohol Consumption", "-"))
        self.user_labels["Activity"].configure(text=user_info.get("Physical Activity", "-"))
        self.user_labels["Sleep Hours"].configure(text=user_info.get("Sleep Hours", "-"))

        #---Prediction ----
        self.prediction_label.configure(text=f"Prediction: {prediction}")
        self.risk_score_label.configure(text=f"Risk Score: {risk_score}/100")
        self.confidence_label.configure(text=f"Confidence: {confidence:.2f}%")
        self.mmse_label.configure(text=f"MMSE Score: {user_info['MMSE']}")
        self.bmi_label.configure(text=f"BMI: {user_info['BMI']}")
        self.interpretation_label.configure(text=interpretation)
        self.recommendation_label.configure(text=self.get_suggestions(prediction))
        self.render_pie_chart(confidence)

    def render_pie_chart(self, confidence):
        from io import BytesIO
        import matplotlib.pyplot as plt
        from PIL import Image

        safe = 100 - confidence
        fig, ax = plt.subplots(figsize=(2.5, 2.5))
        ax.pie([confidence, safe], labels=['Risk', 'Safe'], colors=['#e74c3c', '#2ecc71'], autopct='%1.1f%%')
        ax.axis('equal')

        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)

        try:
            img = Image.open(buf)
            ctk_img = CTkImage(light_image=img, size=(200, 200))
            self.chart_label.configure(image=ctk_img, text="")
            self.chart_label.image = ctk_img
        except Exception as e:
            print(f"Chart render error: {e}")

    def export_pdf(self):
        filename = f"dementia_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        y = height - 50  # Start position

        # === Title ===
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2, y, "Initial Diagnosis of Dementia using Machine Learning Approach")
        y -= 30

        # === Report Metadata ===
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Date: {datetime.now().strftime('%B %d, %Y')}")
        y -= 20
        c.drawString(50, y, f"Report ID: DRX-{random.randint(1000, 9999)}")
        y -= 30

        # === USER DETAILS ===
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "👤 User Details")
        y -= 20
        c.setFont("Helvetica", 12)

        for key in ["Name", "Age", "Gender", "MMSE", "BMI", "Smoking", "Alcohol", "Activity", "Sleep Hours"]:
            label = self.user_labels.get(key)
            if label:
                value = label.cget("text")
                c.drawString(60, y, f"{key}: {value}")
                y -= 20

            # === PREDICTION SUMMARY ===
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "📊 Prediction Summary")
        y -= 20
        c.setFont("Helvetica", 12)

        for label in [
            self.prediction_label,
            self.risk_score_label,
            self.confidence_label,
            self.mmse_label,
            self.bmi_label,
            self.model_accuracy_label
        ]:
            c.drawString(60, y, label.cget("text"))
            y -= 20

        y -= 10

        # === INTERPRETATION ===
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "🩺 Interpretation")
        y -= 20
        c.setFont("Helvetica", 12)
        for line in self.interpretation_label.cget("text").split('\n'):
            c.drawString(60, y, line)
            y -= 20

        y -= 10

        # === RECOMMENDATION ===
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, "📌 Recommendation")
        y -= 20
        c.setFont("Helvetica", 12)
        for line in self.recommendation_label.cget("text").split('\n'):
            c.drawString(60, y, line)
            y -= 20

        c.save()
        messagebox.showinfo("PDF Exported", f"Report saved as {filename}")


    def get_suggestions(self, prediction):
        if "Mild" in prediction:
            return (
                "1. Schedule regular check-ups\n"
                "2. Maintain a balanced diet\n"
                "3. Perform mental stimulation activities\n"
                "4. Engage in low-impact physical exercises\n"
                "5. Establish consistent sleep patterns\n"
                "6. Stay connected with family & friends"
            )
        elif "Dementia" in prediction:
            return (
                "1. Immediate specialist consultation\n"
                "2. Cognitive behavioral therapy\n"
                "3. Supervised care & environment safety\n"
                "4. Support from family/caregivers\n"
                "5. Manage co-existing health conditions"
            )
        else:
            return "No significant signs detected. Maintain a healthy lifestyle and retest periodically."

# ------------------ History Page ------------------
class HistoryPage(BackgroundPage):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # === Project Title at the Top ===
        title_label = ctk.CTkLabel(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                                font=ctk.CTkFont(size=28, weight="bold"),
                                text_color="black", anchor="center")
        title_label.pack(pady=(20, 10))
        # === Title ===
        title = ctk.CTkLabel(self, text="Login History", font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=(20, 10))

        # === User Info Frame ===
        self.user_info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.user_info_frame.pack(pady=(0, 10))

        self.username_label = ctk.CTkLabel(self.user_info_frame, text="Username:", font=ctk.CTkFont(size=16, weight="bold"))
        self.username_label.grid(row=0, column=0, sticky="e", padx=5)
        self.username_value = ctk.CTkLabel(self.user_info_frame, text="", font=ctk.CTkFont(size=16))
        self.username_value.grid(row=0, column=1, sticky="w", padx=5)

        self.email_label = ctk.CTkLabel(self.user_info_frame, text="Email:", font=ctk.CTkFont(size=16, weight="bold"))
        self.email_label.grid(row=1, column=0, sticky="e", padx=5)
        self.email_value = ctk.CTkLabel(self.user_info_frame, text="", font=ctk.CTkFont(size=16))
        self.email_value.grid(row=1, column=1, sticky="w", padx=5)

        # === Table Frame ===
        self.table_frame = ctk.CTkFrame(self, width=700, height=450)
        self.table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # === Stats Label ===
        self.stats_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.stats_label.pack(pady=(5, 0))


        # === Treeview Style ===
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 20))  # <-- change font & size here
        style.configure("Custom.Treeview.Heading", font=("Arial", 20, "bold"))

# === Treeview (Table) ===
        self.tree = ttk.Treeview(self.table_frame, columns=("Date", "Time", "Age", "BMI", "Diagnosis"), show="headings", height=20)
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Time")
        self.tree.heading("Age", text="Age")
        self.tree.heading("BMI", text="BMI")
        #self.tree.heading("MMSE Score:", text="MMSE Score:")
        self.tree.heading("Diagnosis", text="Diagnosis")

        self.tree.column("Date", width=120, anchor="center")
        self.tree.column("Time", width=120, anchor="center")
        self.tree.column("Age", width=80, anchor="center")
        self.tree.column("BMI", width=80, anchor="center")
        #self.tree.column("MMSE Score:", width=80, anchor="center")
        self.tree.column("Diagnosis", width=150, anchor="center")


        # === Scrollbar ===
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        # === Bottom Buttons ===
        bottom_btn_frame = ctk.CTkFrame(self)
        bottom_btn_frame.pack(side="bottom", fill="x", padx=30, pady=20)

        back_btn = ctk.CTkButton(bottom_btn_frame, text="Back", width=150, fg_color="#f0ad4e",
                                 command=lambda: self.controller.show_frame(DashboardPage))
        back_btn.pack(side="left")

        logout_btn = ctk.CTkButton(bottom_btn_frame, text="Logout", width=150, fg_color="#d9534f",
                                   command=self.logout_user)
        logout_btn.pack(side="right")

        # Load data
        self.load_login_history()

    def logout_user(self):
        self.controller.current_user_id = None
        self.controller.latest_prediction = None
        self.controller.show_frame(LoginPage)

    def load_login_history(self):
        user_id = self.controller.current_user_id
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pooji",
                database="dementia_app"
            )
            cursor = conn.cursor()
            # === User Info ===
            cursor.execute("SELECT name, email FROM users WHERE user_id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                name, email = user  # ✅ works only if your SQL is SELECT name, email
                self.username_value.configure(text=name)
                self.email_value.configure(text=email)
            else:
                self.username_value.configure(text="N/A")
                self.email_value.configure(text="N/A")

            # === Login History (age, bmi, etc.)
            cursor.execute("""
                SELECT m.age, m.bmi, m.mmse_score, m.diagnosis, m.created_at
                FROM medical_history m
                JOIN patients p ON m.patient_id = p.patient_id
                WHERE p.user_id = %s
                ORDER BY m.created_at DESC
            """, (user_id,))
            rows = cursor.fetchall()

            self.tree.delete(*self.tree.get_children())
            login_count = 0
            for age, bmi, mmse, diagnosis, ts in rows:
                date_str = ts.strftime("%Y-%m-%d")
                time_str = ts.strftime("%H:%M:%S")
                age = age if age else "-"
                bmi = round(bmi, 2) if bmi else "-"
                diagnosis = diagnosis if diagnosis else "-"
                self.tree.insert("", "end", values=(date_str, time_str, age, bmi, diagnosis))
                login_count += 1

            if login_count == 0:
                self.stats_label.configure(text="No login history available.")
            else:
                self.stats_label.configure(text=f"Total Logins: {login_count}")

        except Exception as e:
            self.username_value.configure(text="Error")
            self.email_value.configure(text=str(e))

   
# ------------------ Run Application ------------------
if __name__ == "__main__":
    app = DementiaApp()
    app.mainloop()