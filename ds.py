import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk
import pandas as pd
import joblib
from datetime import datetime

# Set appearance mode and color theme
ctk.set_appearance_mode("light")  # Can be "light", "dark", or "system"
ctk.set_default_color_theme("blue")  # Other options: "green", "dark-blue"

# ------------------ MySQL Config ------------------
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pooji",
            database="dementia_app"
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
        self.state('zoomed')  # Start maximized (better than fullscreen)
        self.minsize(1000, 700)
        
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
        for F in (MainPage, SecondPage, AbstractPage, AlgorithmPage, 
                 LoginPage, RegisterPage, MedicalTestsPage, ResultPage, HistoryPage):
            page = F(parent=self.container, controller=self)
            self.frames[F] = page
            page.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(MainPage)
        
        # Bind escape key to toggle fullscreen
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.bind("<F11>", lambda e: self.attributes("-fullscreen", True))

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

# ------------------ Base Page ------------------
class BasePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=("white", "#2b2b2b"))  # Light/Dark mode compatible
        
        # Title label common to all pages
        self.title_font = ctk.CTkFont(family="Times New Roman", size=20, weight="bold")
        self.title_label = ctk.CTkLabel(
            self,
            text="Initial Diagnosis of Dementia using Machine Learning Approach",
            font=self.title_font,
            text_color=("black", "white")
        )
        self.title_label.pack(pady=10, padx=10, anchor="center")

# ------------------ Main Page ------------------
class MainPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Logo and title section
        top_frame = ctk.CTkFrame(container, fg_color="transparent")
        top_frame.pack(fill="x", pady=(0, 20))
        
        # Left logo
        try:
            left_logo = Image.open("gvp logo.png").resize((100, 100))
            self.left_logo_img = ImageTk.PhotoImage(left_logo)
            ctk.CTkLabel(top_frame, image=self.left_logo_img, text="").pack(side="left", padx=10)
        except:
            pass
        
        # Center labels
        title_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        title_frame.pack(side="left", expand=True)
        
        ctk.CTkLabel(title_frame, 
                     text="GAYATRI VIDYA PARISHAD",
                     font=ctk.CTkFont(family="Courier", size=22, weight="bold")).pack()
        ctk.CTkLabel(title_frame, 
                     text="COLLEGE FOR DEGREE AND PG COURSES (A)",
                     font=ctk.CTkFont(family="Courier", size=18)).pack()
        ctk.CTkLabel(title_frame, 
                     text="Department of Computer Applications",
                     font=ctk.CTkFont(family="Times New Roman", size=14, weight="bold")).pack()
        
        # Right logo
        try:
            right_logo = Image.open("gvp logo.png").resize((100, 100))
            self.right_logo_img = ImageTk.PhotoImage(right_logo)
            ctk.CTkLabel(top_frame, image=self.right_logo_img, text="").pack(side="right", padx=10)
        except:
            pass
        
        # Project Title
        ctk.CTkLabel(container, 
                     text="Initial Diagnosis of Dementia using Machine Learning Approach",
                     font=ctk.CTkFont(family="Times New Roman", size=20, weight="bold", underline=True),
                     text_color=("black", "white")).pack(pady=20)
        
        # Author & Guide Info
        content_frame = ctk.CTkFrame(container, fg_color="transparent")
        content_frame.pack(pady=10)
        
        author_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        author_frame.pack(side="left", padx=40)
        ctk.CTkLabel(author_frame, 
                     text="By: P. Poojitha\nPG232402030\nMaster of Computer Applications\nSem-IV",
                     justify="left").pack()
        
        guide_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        guide_frame.pack(side="right", padx=40)
        ctk.CTkLabel(guide_frame, 
                     text="Project guide:\nMrs. P. Ratna Pavani\nAssistant Professor\nDept of Computer Applications",
                     justify="right").pack()
        
        # Buttons at bottom
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        
        ctk.CTkButton(bottom_frame, text="Proceed", width=150,
                      command=lambda: controller.show_frame(SecondPage)).pack(side="left", padx=20)
        ctk.CTkButton(bottom_frame, text="Exit", width=150, fg_color="#d9534f",
                      command=self.confirm_exit).pack(side="right", padx=20)

    def confirm_exit(self):
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            self.controller.destroy()

# ------------------ Second Page ------------------
class SecondPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Main container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Left frame for image
        self.left_frame = ctk.CTkFrame(container, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # Right frame for buttons
        self.right_frame = ctk.CTkFrame(container, fg_color="transparent")
        self.right_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # Load image
        try:
            img = Image.open("dementia.jpeg")
            img = img.resize((400, 400), Image.LANCZOS)
            self.dementia_img = ImageTk.PhotoImage(img)
            self.img_label = ctk.CTkLabel(self.left_frame, image=self.dementia_img, text="")
            self.img_label.pack(expand=True)
        except:
            self.img_label = ctk.CTkLabel(self.left_frame, 
                                         text="[Image Placeholder]",
                                         font=ctk.CTkFont(size=20, weight="bold"),
                                         text_color="gray")
            self.img_label.pack(expand=True)
        
        # Buttons container
        buttons_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        buttons_container.pack(expand=True)
        
        # Create buttons with icons
        self.abstract_btn = ctk.CTkButton(
            buttons_container,
            text="Abstract",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=50,
            command=lambda: controller.show_frame(AbstractPage)
        )
        
        self.algorithm_btn = ctk.CTkButton(
            buttons_container,
            text="Algorithm & Example",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=50,
            command=lambda: controller.show_frame(AlgorithmPage)
        )
        
        self.howto_btn = ctk.CTkButton(
            buttons_container,
            text="How to Use",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=50,
            command=lambda: messagebox.showinfo("How to Use", "Usage instructions here")
        )
        
        # Pack buttons
        self.abstract_btn.pack(pady=10)
        self.algorithm_btn.pack(pady=10)
        self.howto_btn.pack(pady=10)
        
        # Bottom buttons
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", pady=10)
        
        ctk.CTkButton(bottom_frame, text="Login", width=150,
                      command=lambda: controller.show_frame(LoginPage)).pack(side="right", padx=20)
        ctk.CTkButton(bottom_frame, text="Back", width=150,
                      command=lambda: controller.show_frame(MainPage)).pack(side="right", padx=20)
        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        width = event.width
        height = event.height
        
        # Adjust layout based on window size
        if width < 800:  # Switch to vertical layout
            self.left_frame.pack_forget()
            self.right_frame.pack_forget()
            self.left_frame.pack(side="top", fill="both", expand=True, pady=10)
            self.right_frame.pack(side="top", fill="both", expand=True, pady=10)
        else:  # Horizontal layout
            self.left_frame.pack_forget()
            self.right_frame.pack_forget()
            self.left_frame.pack(side="left", fill="both", expand=True, padx=10)
            self.right_frame.pack(side="left", fill="both", expand=True, padx=10)

# ------------------ Abstract Page ------------------
class AbstractPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(container, text="Abstract", 
                     font=ctk.CTkFont(family="Courier", size=20, underline=True)).pack(pady=10)
        
        content = (
            "Dementia is a brain disorder that affects memory, thinking, and daily life. Early diagnosis is "
            "crucial for timely treatment and better patient care. Traditional methods like cognitive tests "
            "and brain scans are often slow, expensive, and require medical experts, leading to delayed diagnosis. "
            "Some AI methods, such as SVM and k-NN, struggle with handling large datasets and achieving high accuracy. "
            "This project proposes using the Random Forest algorithm for early dementia detection. It analyzes patient "
            "data, including memory test results, lifestyle, and medical history, to predict dementia risk efficiently. "
            "Random Forest is effective in handling large medical datasets, avoiding overfitting, and providing high accuracy. "
            "The model offers a reliable, cost-effective, and automated solution for detecting dementia at an early stage."
        )
        
        textbox = ctk.CTkTextbox(container, width=800, height=300, 
                                font=ctk.CTkFont(size=12), wrap="word")
        textbox.insert("1.0", content)
        textbox.configure(state="disabled")
        textbox.pack(pady=10)
        
        ctk.CTkButton(self, text="Back", width=150, fg_color="#d9534f",
                      command=lambda: controller.show_frame(SecondPage)).pack(pady=10)

# ------------------ Algorithm Page ------------------
class AlgorithmPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(container, text="Algorithm", 
                     font=ctk.CTkFont(family="Courier", size=20, underline=True)).pack(pady=10)
        
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
        
        textbox = ctk.CTkTextbox(container, width=800, height=300, 
                                font=ctk.CTkFont(size=12), wrap="word")
        textbox.insert("1.0", content)
        textbox.configure(state="disabled")
        textbox.pack(pady=10)
        
        ctk.CTkButton(self, text="Back", width=150, fg_color="#d9534f",
                      command=lambda: controller.show_frame(SecondPage)).pack(pady=10)

# ------------------ Login Page ------------------
class LoginPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(container, text="Login", 
                     font=ctk.CTkFont(size=20)).pack(pady=20)
        
        # Form frame
        form_frame = ctk.CTkFrame(container, fg_color="transparent")
        form_frame.pack(pady=20)
        
        # Username field
        ctk.CTkLabel(form_frame, text="Username").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(form_frame, width=250)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Password field
        ctk.CTkLabel(form_frame, text="Password").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(form_frame, width=250, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="Login", width=150,
                      command=self.check_login).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="New User? Register", width=150,
                      command=lambda: controller.show_frame(RegisterPage)).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Back", width=150,
                      command=lambda: controller.show_frame(SecondPage)).pack(side="left", padx=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT user_id FROM users WHERE username=%s AND password=%s", 
                              (username, password))
                result = cursor.fetchone()
                
                if result:
                    user_id = result[0]
                    # Store user_id in controller for later use
                    self.controller.current_user_id = user_id
                    
                    # Record login history
                    cursor.execute("""
                        INSERT INTO login_history (user_id, ip_address)
                        VALUES (%s, '127.0.0.1')
                    """, (user_id,))
                    conn.commit()
                    
                    messagebox.showinfo("Success", f"Welcome {username}!")
                    self.controller.frames[MedicalTestsPage].set_username(username)
                    self.controller.show_frame(MedicalTestsPage)
                else:
                    messagebox.showerror("Error", "Invalid username or password")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                conn.close()

# ------------------ Register Page ------------------
class RegisterPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(pady=20, padx=40, fill="both", expand=True)
        
        ctk.CTkLabel(container, text="Register New User", 
                     font=ctk.CTkFont(size=20)).pack(pady=20)
        
        # Form frame
        form_frame = ctk.CTkFrame(container, fg_color="transparent")
        form_frame.pack(pady=20)
        
        # Form fields
        fields = ["Name", "Email", "Username", "Password", "Confirm Password"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            ctk.CTkLabel(form_frame, text=field).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=250, show="*" if "Password" in field else None)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry
        
        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="Register", width=150,
                      command=self.register_user).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Back", width=150,
                      command=lambda: controller.show_frame(LoginPage)).pack(side="left", padx=10)

    def register_user(self):
        data = {key: entry.get().strip() for key, entry in self.entries.items()}
        
        # Validation
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
            
        # Insert user
        if insert_user(data["Name"], data["Email"], data["Username"], data["Password"]):
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.controller.show_frame(LoginPage)

# ------------------ Medical Tests Page ------------------
class MedicalTestsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.username = ""
        
        # Main container with scrollbar
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to scroll
        self.canvas.bind_all("<MouseWheel>", 
                           lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        
        # Welcome label
        self.welcome_label = ctk.CTkLabel(
            self.scrollable_frame, 
            text="",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.welcome_label.pack(pady=20)
        
        # Form container
        form_container = ctk.CTkFrame(self.scrollable_frame)
        form_container.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Form fields
        self.fields = {}
        
        # Gender
        ctk.CTkLabel(form_container, text="Gender:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.gender_var = ctk.StringVar(value="Select")
        gender_menu = ctk.CTkOptionMenu(form_container, 
                                       values=["Male", "Female"],
                                       variable=self.gender_var)
        gender_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Age
        ctk.CTkLabel(form_container, text="Age:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.age_entry = ctk.CTkEntry(form_container)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # MMSE Test Score
        ctk.CTkLabel(form_container, text="MMSE Test Score:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.mmse_entry = ctk.CTkEntry(form_container)
        self.mmse_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Weight
        ctk.CTkLabel(form_container, text="Weight (kg):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.weight_entry = ctk.CTkEntry(form_container)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Height
        ctk.CTkLabel(form_container, text="Height (cm):").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.height_entry = ctk.CTkEntry(form_container)
        self.height_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w")
        
        # Smoking
        ctk.CTkLabel(form_container, text="Smoking:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.smoking_var = ctk.StringVar(value="Select")
        smoking_menu = ctk.CTkOptionMenu(form_container, 
                                        values=["Yes", "No"],
                                        variable=self.smoking_var)
        smoking_menu.grid(row=5, column=1, padx=10, pady=10, sticky="w")
        
        # Alcohol
        ctk.CTkLabel(form_container, text="Alcohol Consumption:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.alcohol_var = ctk.StringVar(value="Select")
        alcohol_menu = ctk.CTkOptionMenu(form_container, 
                                        values=["Yes", "No"],
                                        variable=self.alcohol_var)
        alcohol_menu.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        
        # Physical Activity
        ctk.CTkLabel(form_container, text="Physical Activity:").grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.activity_var = ctk.StringVar(value="Select")
        activity_menu = ctk.CTkOptionMenu(form_container, 
                                         values=["Low", "Moderate", "High"],
                                         variable=self.activity_var)
        activity_menu.grid(row=7, column=1, padx=10, pady=10, sticky="w")
        
        # Sleep Hours
        ctk.CTkLabel(form_container, text="Sleep Hours:").grid(row=8, column=0, padx=10, pady=10, sticky="e")
        self.sleep_entry = ctk.CTkEntry(form_container)
        self.sleep_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")
        
        # Button frame
        button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="Clear", width=150, fg_color="#f0ad4e",
                      command=self.clear_fields).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Submit", width=150,
                      command=self.submit_data).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Predict Diagnosis", width=150,
                      command=self.predict_dementia).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Back", width=150, fg_color="#d9534f",
                      command=lambda: self.controller.show_frame(SecondPage)).pack(side="left", padx=10)
    
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
                        SET gender=%s, age=%s, weight=%s, height=%s, bmi=%s,
                            smoking=%s, alcohol=%s, physical_activity=%s, sleep_hours=%s, mmse_score=%s
                        WHERE user_id=%s
                    """, (
                        self.gender_var.get(), age, float(self.weight_entry.get()), 
                        float(self.height_entry.get()), bmi, self.smoking_var.get(),
                        self.alcohol_var.get(), self.activity_var.get(), sleep_hours, mmse_score,
                        self.controller.current_user_id
                    ))
                else:
                    # Insert new patient
                    cursor.execute("""
                        INSERT INTO patients 
                        (user_id, gender, age, weight, height, bmi, smoking, alcohol, 
                         physical_activity, sleep_hours, mmse_score)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        self.controller.current_user_id, self.gender_var.get(), age, 
                        float(self.weight_entry.get()), float(self.height_entry.get()), bmi,
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
        # Validate all dropdowns first
        if (self.gender_var.get() == "Select" or 
            self.smoking_var.get() == "Select" or 
            self.alcohol_var.get() == "Select" or 
            self.activity_var.get() == "Select"):
            messagebox.showerror("Error", "Please select all dropdown options")
            return None

        try:
            # Validate numeric fields
            age = self.validate_numeric_input(self.age_entry.get(), "Age")
            mmse_score = self.validate_numeric_input(self.mmse_entry.get(), "MMSE Score")
            weight = self.validate_numeric_input(self.weight_entry.get(), "Weight", allow_float=True)
            height = self.validate_numeric_input(self.height_entry.get(), "Height", allow_float=True)
            sleep_hours = self.validate_numeric_input(self.sleep_entry.get(), "Sleep Hours", allow_float=True)
            
            if None in (age, mmse_score, weight, height, sleep_hours):
                return None

            # Additional validation
            if not (0 <= mmse_score <= 30):
                messagebox.showerror("Error", "MMSE Score must be between 0-30")
                return None
                
            if height <= 0:
                messagebox.showerror("Error", "Height must be positive")
                return None

            bmi = weight / ((height/100) ** 2)
            
            gender = 1 if self.gender_var.get() == "Male" else 0
            smoking = 1 if self.smoking_var.get() == "Yes" else 0
            alcohol = 1 if self.alcohol_var.get() == "Yes" else 0
            activity = {"Low": 0, "Moderate": 1, "High": 2}[self.activity_var.get()]

            return pd.DataFrame([[gender, age, mmse_score, bmi, smoking, alcohol, activity, sleep_hours]], 
                            columns=self.controller.feature_columns)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            return None
    def predict_dementia(self):
        user_data = self.get_user_inputs()
        if user_data is not None:
            # Make prediction
            prediction = self.controller.model.predict(user_data)
            probability = self.controller.model.predict_proba(user_data)[0]
            
            # Save prediction to database
            try:
                conn = connect_db()
                if conn:
                    cursor = conn.cursor()
                    
                    # Get patient_id
                    cursor.execute("SELECT patient_id FROM patients WHERE user_id=%s", 
                                  (self.controller.current_user_id,))
                    patient_id = cursor.fetchone()[0]
                    
                    # Save prediction
                    diagnosis = "High Risk" if prediction[0] == 1 else "Low Risk"
                    cursor.execute("""
                        INSERT INTO medical_history 
                        (patient_id, diagnosis, diagnosis_date, notes)
                        VALUES (%s, %s, %s, %s)
                    """, (
                        patient_id, diagnosis, datetime.now().date(),
                        f"Prediction probability: {probability[1]:.2f}"
                    ))
                    conn.commit()
                    
                    # Prepare result data for ResultsPage
                    result_data = {
                        "username": self.username,
                        "gender": self.gender_var.get(),
                        "age": self.age_entry.get(),
                        "mmse_score": self.mmse_entry.get(),
                        "bmi": self.calculate_bmi(),
                        "smoking": self.smoking_var.get(),
                        "alcohol": self.alcohol_var.get(),
                        "activity": self.activity_var.get(),
                        "sleep": self.sleep_entry.get(),
                        "diagnosis": diagnosis,
                        "probability": f"{probability[1]*100:.2f}%",
                        "suggestions": self.get_suggestions(prediction[0])
                    }
                    
                    # Show results page
                    self.controller.frames[ResultPage].display_results(result_data)
                    self.controller.show_frame(ResultPage)
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))
            finally:
                if conn:
                    conn.close()
    
    def get_suggestions(self, prediction):
        if prediction == 1:  # High risk
            return (
                "1. Consult a neurologist or geriatric specialist immediately\n"
                "2. Regular cognitive exercises and brain training\n"
                "3. Maintain a healthy Mediterranean-style diet\n"
                "4. Engage in regular physical activity\n"
                "5. Ensure proper sleep hygiene\n"
                "6. Social engagement and mental stimulation"
            )
        else:  # Low risk
            return (
                "1. Continue healthy lifestyle habits\n"
                "2. Regular cognitive check-ups\n"
                "3. Balanced diet rich in omega-3 fatty acids\n"
                "4. Regular physical exercise\n"
                "5. Mental stimulation through learning new skills\n"
                "6. Maintain social connections"
            )

# ------------------ Result Page ------------------
class ResultPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.result_data = None
        
        # Main container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Will be populated by display_results
    def display_results(self, result_data):
        self.result_data = result_data
        
        # Clear previous widgets
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Results title
        ctk.CTkLabel(self.container, 
                    text="Diagnosis Results",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Patient information frame
        info_frame = ctk.CTkFrame(self.container)
        info_frame.pack(pady=10, padx=20, fill="x")
        
        # Display patient info
        ctk.CTkLabel(info_frame, 
                    text=f"Patient: {result_data['username']}",
                    font=ctk.CTkFont(size=16)).pack(anchor="w", pady=5)
        
        ctk.CTkLabel(info_frame, 
                    text=f"Age: {result_data['age']} | Gender: {result_data['gender']}",
                    font=ctk.CTkFont(size=14)).pack(anchor="w", pady=5)
        
        # Diagnosis frame
        diagnosis_frame = ctk.CTkFrame(self.container)
        diagnosis_frame.pack(pady=20, padx=20, fill="x")
        
        # Diagnosis result with color coding
        if "High" in result_data['diagnosis']:
            diagnosis_color = "#d9534f"  # Red for high risk
        else:
            diagnosis_color = "#5cb85c"  # Green for low risk
            
        ctk.CTkLabel(diagnosis_frame, 
                    text=f"Diagnosis: {result_data['diagnosis']}",
                    font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=diagnosis_color).pack(pady=10)
        
        ctk.CTkLabel(diagnosis_frame, 
                    text=f"Probability: {result_data['probability']}",
                    font=ctk.CTkFont(size=16)).pack(pady=5)
        
        # Suggestions frame
        suggestions_frame = ctk.CTkFrame(self.container)
        suggestions_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(suggestions_frame, 
                    text="Recommendations:",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        suggestions_text = ctk.CTkTextbox(suggestions_frame, 
                                        width=600, 
                                        height=200,
                                        font=ctk.CTkFont(size=14),
                                        wrap="word")
        suggestions_text.insert("1.0", result_data['suggestions'])
        suggestions_text.configure(state="disabled")
        suggestions_text.pack(pady=10)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="View History", width=150,
                     command=lambda: self.controller.show_frame(HistoryPage)).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Logout", width=150, fg_color="#d9534f",
                     command=lambda: self.controller.show_frame(SecondPage)).pack(side="left", padx=10)

# ------------------ History Page ------------------
class HistoryPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Main container with scrollbar
        self.canvas = ctk.CTkCanvas(self, highlightthickness=0)
        self.scrollbar = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = ctk.CTkFrame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to scroll
        self.canvas.bind_all("<MouseWheel>", 
                           lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
        
        # Title
        ctk.CTkLabel(self.scrollable_frame, 
                    text="Prediction History",
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=20)
        
        # Will be populated by load_history
        self.history_container = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.history_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Button frame
        button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        ctk.CTkButton(button_frame, text="Back", width=150,
                     command=lambda: self.controller.show_frame(ResultPage)).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Logout", width=150, fg_color="#d9534f",
                     command=lambda: self.controller.show_frame(SecondPage)).pack(side="left", padx=10)
    
    def on_show(self):
        self.load_history()
    
    def load_history(self):
        # Clear previous history
        for widget in self.history_container.winfo_children():
            widget.destroy()
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Get patient_id
                cursor.execute("""
                    SELECT p.patient_id, p.gender, p.age 
                    FROM patients p 
                    WHERE p.user_id = %s
                """, (self.controller.current_user_id,))
                patient = cursor.fetchone()
                
                if patient:
                    patient_id, gender, age = patient
                    
                    # Display patient info
                    patient_frame = ctk.CTkFrame(self.history_container)
                    patient_frame.pack(fill="x", pady=10, padx=20)
                    
                    ctk.CTkLabel(patient_frame, 
                                text=f"Patient: {gender}, {age} years old",
                                font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
                    
                    # Get prediction history
                    cursor.execute("""
                        SELECT diagnosis, diagnosis_date, notes 
                        FROM medical_history 
                        WHERE patient_id = %s 
                        ORDER BY diagnosis_date DESC
                    """, (patient_id,))
                    history = cursor.fetchall()
                    
                    if history:
                        for i, (diagnosis, date, notes) in enumerate(history):
                            # History item frame
                            history_frame = ctk.CTkFrame(self.history_container)
                            history_frame.pack(fill="x", pady=10, padx=20)
                            
                            # Color based on diagnosis
                            bg_color = "#f2dede" if "High" in diagnosis else "#dff0d8"
                            fg_color = "#a94442" if "High" in diagnosis else "#3c763d"
                            
                            history_frame.configure(fg_color=bg_color)
                            
                            # Diagnosis and date
                            top_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
                            top_frame.pack(fill="x", pady=5, padx=10)
                            
                            ctk.CTkLabel(top_frame, 
                                        text=f"Diagnosis: {diagnosis}",
                                        font=ctk.CTkFont(size=14, weight="bold"),
                                        text_color=fg_color).pack(side="left")
                            
                            ctk.CTkLabel(top_frame, 
                                        text=f"Date: {date}",
                                        font=ctk.CTkFont(size=12),
                                        text_color=fg_color).pack(side="right")
                            
                            # Notes
                            notes_frame = ctk.CTkFrame(history_frame, fg_color="transparent")
                            notes_frame.pack(fill="x", pady=5, padx=10)
                            
                            ctk.CTkLabel(notes_frame, 
                                        text=f"Notes: {notes}",
                                        font=ctk.CTkFont(size=12),
                                        text_color=fg_color).pack(anchor="w")
                    else:
                        ctk.CTkLabel(self.history_container, 
                                    text="No prediction history found",
                                    font=ctk.CTkFont(size=14)).pack(pady=20)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                conn.close()

# ------------------ Run Application ------------------
if __name__ == "__main__":
    # Check if model files exist
    try:
        # Try loading model files to verify they exist
        joblib.load("dementia_model.pkl")
        joblib.load("model_features.pkl")
        
        # If successful, run the app
        app = DementiaApp()
        app.mainloop()
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"Model file not found: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load model: {e}")