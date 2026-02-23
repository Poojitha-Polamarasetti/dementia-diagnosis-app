import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox,ttk
import mysql.connector
from PIL import Image, ImageTk
import pandas as pd
import joblib
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pooji",  # ✅ Replace with your actual MySQL password
        database="dementia_app"  # ✅ Replace with your actual DB name
    )

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

        '''for F in (MainPage, SecondPage, AbstractPage, AlgorithmPage, 
                 LoginPage, RegisterPage, MedicalTestsPage, ResultPage, HistoryPage):
            page = F(parent=self.container, controller=self)
            self.frames[F] = page
            page.grid(row=0, column=0, sticky="nsew")'''
        
        self.show_frame(MainPage)
        
        # Bind escape key to toggle fullscreen
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", True))
        self.bind("<F11>", lambda e: self.attributes("-fullscreen", True))

    def show_frame(self, page_class):
        """Creates and raises a frame dynamically to prevent flashing."""
        if page_class not in self.frames:
            self.frames[page_class] = page_class(parent=self.container, controller=self)
            self.frames[page_class].grid(row=0, column=0, sticky="nsew")

        frame = self.frames[page_class]
        frame.tkraise()

        if hasattr(frame, "on_show"):
            frame.on_show()

# ------------------ Base Page ------------------
class BasePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color=( "#d0e7f9"))  # Light/Dark mode compatible
        
        # Title label common to all pages
        self.title_font = ctk.CTkFont(family="Times New Roman", size=24, weight="bold")
        if self.__class__.__name__ != "MainPage":
            self.title_font = ctk.CTkFont(family="Times New Roman", size=24, weight="bold")
            self.title_label = ctk.CTkLabel(
                self,
                text="Initial Diagnosis of Dementia using Machine Learning Approach",
                font=self.title_font,
                text_color=("black", "white")
            )
            self.title_label.pack(pady=10, padx=10, anchor="center")

        
        # Bind resize event
        self.bind("<Configure>", self.on_resize)
    
    def on_resize(self, event):
        # Base responsive behavior - can be overridden by child classes
        width = event.width
        height = event.height
        
        # Adjust font sizes based on window dimensions
        if width < 1000 or height < 700:
            # Smaller window - reduce font sizes
            self.title_font.configure(size=30)
        else:
            # Larger window - normal font sizes
            self.title_font.configure(size=40)

# ------------------ Main Page ------------------
class MainPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        self.configure(fg_color="#f0f8ff")  # Light blue background

        # === Main content container ===
        self.container = ctk.CTkFrame(self, fg_color="white", corner_radius=20)
        self.container.pack(pady=40, padx=60, fill="both", expand=True)

        # === Header with logos and title side by side ===
        header_frame = ctk.CTkFrame(self.container, fg_color="white")
        header_frame.pack(pady=20, padx=20, fill="x")

        # Left Logo
        try:
            left_logo = Image.open("gvp logo.png").resize((100, 100))
            self.left_logo_img = ImageTk.PhotoImage(left_logo)
            tk.Label(header_frame, image=self.left_logo_img, bg="white").pack(side="left", padx=10)
        except:
            tk.Label(header_frame, text="[LOGO]", bg="white").pack(side="left", padx=10)

        # Center title info
        title_frame = ctk.CTkFrame(header_frame, fg_color="white")
        title_frame.pack(side="left", expand=True)

        ctk.CTkLabel(title_frame, text="GAYATRI VIDYA PARISHAD", 
                     font=("Times New Roman", 40, "bold"), text_color="black").pack(pady=(0, 5))
        ctk.CTkLabel(title_frame, text="COLLEGE FOR DEGREE AND PG COURSES (A)", 
                     font=("Times New Roman", 36, "bold"), text_color="black").pack(pady=(0, 5))
        ctk.CTkLabel(title_frame, text="Department of Computer Applications", 
                     font=("Times New Roman", 30), text_color="black").pack(pady=(0, 10))

        # Right Logo
        try:
            right_logo = Image.open("gvp logo.png").resize((100, 100))
            self.right_logo_img = ImageTk.PhotoImage(right_logo)
            tk.Label(header_frame, image=self.right_logo_img, bg="white").pack(side="right", padx=10)
        except:
            tk.Label(header_frame, text="[LOGO]", bg="white").pack(side="right", padx=10)

        # === Project Title ===
        ctk.CTkLabel(self.container, 
                     text="Initial Diagnosis of Dementia using Machine Learning Approach",
                     font=("Times New Roman", 34, "bold"), wraplength=700, justify="center",
                     text_color="black").pack(pady=30)

        # === Author & Guide Info ===
        info_frame = ctk.CTkFrame(self.container, fg_color="white")
        info_frame.pack(pady=10)

        # Left: Student Info
        left_box = ctk.CTkFrame(info_frame, fg_color="white")
        left_box.pack(side="left", padx=80)

        ctk.CTkLabel(left_box, text="By:", font=("Arial", 20, "bold"), text_color="black").pack(pady=2)
        ctk.CTkLabel(left_box, text="Polamarasetti Poojitha", font=("Arial", 20), text_color="black").pack(pady=2)
        ctk.CTkLabel(left_box, text="PG232402030 – MCA", font=("Arial", 20), text_color="black").pack(pady=2)
        ctk.CTkLabel(left_box, text="Sem- IV", font=("Arial", 20), text_color="black").pack(pady=2)


        # Right: Guide Info
        right_box = ctk.CTkFrame(info_frame, fg_color="white")
        right_box.pack(side="left", padx=80)

        ctk.CTkLabel(right_box, text="Project guide:", font=("Arial", 20, "bold"), text_color="black").pack(pady=2)
        ctk.CTkLabel(right_box, text="Mrs. P. Ratna Pavani", font=("Arial", 20), text_color="black").pack(pady=2)
        ctk.CTkLabel(right_box, text="Assistant Professor", font=("Arial", 20), text_color="black").pack(pady=2)
        ctk.CTkLabel(right_box, text="Dept of Computer Applications", font=("Arial", 20), text_color="black").pack(pady=2)


        # === Bottom Navigation Buttons ===
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.pack(side="bottom", fill="x", pady=20)

        proceed_btn = ctk.CTkButton(bottom_frame, text="Proceed", width=180,height=50,
                                    command=lambda: controller.show_frame(SecondPage))
        proceed_btn.pack(side="left", padx=50)

        exit_btn = ctk.CTkButton(bottom_frame, text="Exit", width=180,height=50, fg_color="#d9534f",
                                 command=self.confirm_exit)
        exit_btn.pack(side="right", padx=40)

    def confirm_exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.controller.destroy()


# ------------------ Second Page ------------------
class SecondPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        # Main container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Left frame for image
        self.left_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        
        # Right frame for buttons
        self.right_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        
        # Load image
        try:
            self.dementia_img = Image.open("dementia.jpeg")
            self.dementia_img_tk = ImageTk.PhotoImage(self.dementia_img)
            self.img_label = ctk.CTkLabel(self.left_frame, image=self.dementia_img_tk, text="")
            self.img_label.pack(expand=True)
        except:
            self.img_label = ctk.CTkLabel(self.left_frame, 
                                         text="[Image Placeholder]",
                                         font=ctk.CTkFont(size=20, weight="bold"),
                                         text_color="gray")
            self.img_label.pack(expand=True)
        
        # Buttons container
        self.buttons_container = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.buttons_container.pack(expand=True)
        
        # Create buttons with icons
        self.abstract_btn = ctk.CTkButton(
            self.buttons_container,
            text="Abstract",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=50,
            command=lambda: controller.show_frame(AbstractPage)
        )
        
        self.algorithm_btn = ctk.CTkButton(
            self.buttons_container,
            text="Algorithm & Example",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=200,
            height=50,
            command=lambda: controller.show_frame(AlgorithmPage)
        )
        
        self.howto_btn = ctk.CTkButton(
            self.buttons_container,
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
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(side="bottom", fill="x", pady=10)
        
        self.login_btn = ctk.CTkButton(self.bottom_frame, text="Login", width=150,
                      command=lambda: controller.show_frame(LoginPage))
        self.login_btn.pack(side="right", padx=20)
        
        self.back_btn = ctk.CTkButton(self.bottom_frame, text="Back", width=150,
                      command=lambda: controller.show_frame(MainPage))
        self.back_btn.pack(side="right", padx=20)
        
        # Initial layout
        self.on_resize(None)
    
    def on_resize(self, event):
        width = self.winfo_width() if event is None else event.width
        height = self.winfo_height() if event is None else event.height
        
        # Clear current layout
        self.left_frame.pack_forget()
        self.right_frame.pack_forget()
        
        # Adjust layout based on window size
        if width < 800:  # Switch to vertical layout
            self.left_frame.pack(side="top", fill="both", expand=True, pady=10)
            self.right_frame.pack(side="top", fill="both", expand=True, pady=10)
            
            # Adjust image size for smaller screens
            try:
                new_size = (min(300, width-40), min(300, height//2))
                resized_img = self.dementia_img.resize(new_size, Image.LANCZOS)
                self.dementia_img_tk = ImageTk.PhotoImage(resized_img)
                self.img_label.configure(image=self.dementia_img_tk)
            except:
                pass
            
            # Adjust button sizes
            btn_width = min(200, width-40)
            self.abstract_btn.configure(width=btn_width)
            self.algorithm_btn.configure(width=btn_width)
            self.howto_btn.configure(width=btn_width)
            
        else:  # Horizontal layout
            self.left_frame.pack(side="left", fill="both", expand=True, padx=10)
            self.right_frame.pack(side="left", fill="both", expand=True, padx=10)
            
            # Adjust image size for larger screens
            try:
                new_size = (min(400, width//2), min(400, height-100))
                resized_img = self.dementia_img.resize(new_size, Image.LANCZOS)
                self.dementia_img_tk = ImageTk.PhotoImage(resized_img)
                self.img_label.configure(image=self.dementia_img_tk)
            except:
                pass
            
            # Reset button sizes
            self.abstract_btn.configure(width=200)
            self.algorithm_btn.configure(width=200)
            self.howto_btn.configure(width=200)
        
        # Adjust bottom buttons
        if width < 600:
            self.login_btn.configure(width=120)
            self.back_btn.configure(width=120)
        else:
            self.login_btn.configure(width=150)
            self.back_btn.configure(width=150)

# ------------------ Abstract Page ------------------
class AbstractPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(self.container, text="Abstract", 
                     font=ctk.CTkFont(family="Courier", size=20, underline=True))
        self.title_label.pack(pady=10)
        
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
        
        self.textbox = ctk.CTkTextbox(self.container, width=800, height=300, 
                                font=ctk.CTkFont(size=12), wrap="word")
        self.textbox.insert("1.0", content)
        self.textbox.configure(state="disabled")
        self.textbox.pack(pady=10)
        
        self.back_btn = ctk.CTkButton(self, text="Back", width=150, fg_color="#d9534f",
                      command=lambda: controller.show_frame(SecondPage))
        self.back_btn.pack(pady=10)
    
    def on_resize(self, event):
        super().on_resize(event)
        width = self.winfo_width() if event is None else event.width
        height = self.winfo_height() if event is None else event.height
        
        # Adjust textbox size
        if width < 1000 or height < 700:
            self.textbox.configure(width=width-100, height=height//2)
            self.back_btn.configure(width=120)
        else:
            self.textbox.configure(width=800, height=300)
            self.back_btn.configure(width=150)

# ------------------ Algorithm Page ------------------
class AlgorithmPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(self.container, text="Algorithm", 
                     font=ctk.CTkFont(family="Courier", size=20, underline=True))
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
        
        self.textbox = ctk.CTkTextbox(self.container, width=800, height=300, 
                                font=ctk.CTkFont(size=12), wrap="word")
        self.textbox.insert("1.0", content)
        self.textbox.configure(state="disabled")
        self.textbox.pack(pady=10)
        
        self.back_btn = ctk.CTkButton(self, text="Back", width=150, fg_color="#d9534f",
                      command=lambda: controller.show_frame(SecondPage))
        self.back_btn.pack(pady=10)
    
    def on_resize(self, event):
        super().on_resize(event)
        width = self.winfo_width() if event is None else event.width
        height = self.winfo_height() if event is None else event.height
        
        # Adjust textbox size
        if width < 1000 or height < 700:
            self.textbox.configure(width=width-100, height=height//2)
            self.back_btn.configure(width=120)
        else:
            self.textbox.configure(width=800, height=300)
            self.back_btn.configure(width=150)

# ------------------ Login Page ------------------
class LoginPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(self.container, text="Login", 
                     font=ctk.CTkFont(size=20))
        self.title_label.pack(pady=20)
        
        # Form frame
        self.form_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.form_frame.pack(pady=20)
        
        # Username field
        ctk.CTkLabel(self.form_frame, text="Username").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = ctk.CTkEntry(self.form_frame, width=250)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Password field
        ctk.CTkLabel(self.form_frame, text="Password").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ctk.CTkEntry(self.form_frame, width=250, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.button_frame.pack(pady=20)
        
        self.login_btn = ctk.CTkButton(self.button_frame, text="Login", width=150,
                      command=self.check_login)
        self.login_btn.pack(side="left", padx=10)
        
        self.register_btn = ctk.CTkButton(self.button_frame, text="New User? Register", width=150,
                      command=lambda: controller.show_frame(RegisterPage))
        self.register_btn.pack(side="left", padx=10)
        
        self.back_btn = ctk.CTkButton(self.button_frame, text="Back", width=150,
                      command=lambda: controller.show_frame(SecondPage))
        self.back_btn.pack(side="left", padx=10)
    
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
    
    def on_resize(self, event):
        super().on_resize(event)
        width = self.winfo_width() if event is None else event.width
        height = self.winfo_height() if event is None else event.height
        
        # Adjust form and button sizes
        if width < 800 or height < 600:
            # Smaller window
            self.username_entry.configure(width=200)
            self.password_entry.configure(width=200)
            
            self.login_btn.configure(width=120)
            self.register_btn.configure(width=120)
            self.back_btn.configure(width=120)
            
            # Stack buttons vertically if needed
            if width < 600:
                self.login_btn.pack_forget()
                self.register_btn.pack_forget()
                self.back_btn.pack_forget()
                
                self.login_btn.pack(pady=5)
                self.register_btn.pack(pady=5)
                self.back_btn.pack(pady=5)
            else:
                # Ensure horizontal layout
                self.login_btn.pack_forget()
                self.register_btn.pack_forget()
                self.back_btn.pack_forget()
                
                self.login_btn.pack(side="left", padx=10)
                self.register_btn.pack(side="left", padx=10)
                self.back_btn.pack(side="left", padx=10)
        else:
            # Larger window - reset to defaults
            self.username_entry.configure(width=250)
            self.password_entry.configure(width=250)
            
            self.login_btn.configure(width=150)
            self.register_btn.configure(width=150)
            self.back_btn.configure(width=150)
            
            # Ensure horizontal layout
            self.login_btn.pack_forget()
            self.register_btn.pack_forget()
            self.back_btn.pack_forget()
            
            self.login_btn.pack(side="left", padx=10)
            self.register_btn.pack(side="left", padx=10)
            self.back_btn.pack(side="left", padx=10)

# ------------------ Register Page ------------------
class RegisterPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(self.container, text="Register New User", 
                     font=ctk.CTkFont(size=20))
        self.title_label.pack(pady=20)
        
        # Form frame
        self.form_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.form_frame.pack(pady=20)
        
        # Form fields
        fields = ["Name", "Email", "Username", "Password", "Confirm Password"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            ctk.CTkLabel(self.form_frame, text=field).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            entry = ctk.CTkEntry(self.form_frame, width=250, show="*" if "Password" in field else None)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.button_frame.pack(pady=20)
        
        self.register_btn = ctk.CTkButton(self.button_frame, text="Register", width=150,
                      command=self.register_user)
        self.register_btn.pack(side="left", padx=10)
        
        self.back_btn = ctk.CTkButton(self.button_frame, text="Back", width=150,
                      command=lambda: controller.show_frame(LoginPage))
        self.back_btn.pack(side="left", padx=10)
    
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
    
    def on_resize(self, event):
        super().on_resize(event)
        width = self.winfo_width() if event is None else event.width
        height = self.winfo_height() if event is None else event.height
        
        # Adjust form and button sizes
        if width < 800 or height < 600:
            # Smaller window
            for entry in self.entries.values():
                entry.configure(width=200)
            
            self.register_btn.configure(width=120)
            self.back_btn.configure(width=120)
            
            # Stack buttons vertically if needed
            if width < 500:
                self.register_btn.pack_forget()
                self.back_btn.pack_forget()
                
                self.register_btn.pack(pady=5)
                self.back_btn.pack(pady=5)
            else:
                # Ensure horizontal layout
                self.register_btn.pack_forget()
                self.back_btn.pack_forget()
                
                self.register_btn.pack(side="left", padx=10)
                self.back_btn.pack(side="left", padx=10)
        else:
            # Larger window - reset to defaults
            for entry in self.entries.values():
                entry.configure(width=250)
            
            self.register_btn.configure(width=150)
            self.back_btn.configure(width=150)
            
            # Ensure horizontal layout
            self.register_btn.pack_forget()
            self.back_btn.pack_forget()
            
            self.register_btn.pack(side="left", padx=10)
            self.back_btn.pack(side="left", padx=10)

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
        self.form_container = ctk.CTkFrame(self.scrollable_frame)
        self.form_container.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Form fields
        self.fields = {}
        
        # Gender
        ctk.CTkLabel(self.form_container, text="Gender:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.gender_var = ctk.StringVar(value="Select")
        self.gender_menu = ctk.CTkOptionMenu(self.form_container, 
                                       values=["Male", "Female"],
                                       variable=self.gender_var)
        self.gender_menu.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Age
        ctk.CTkLabel(self.form_container, text="Age:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.age_entry = ctk.CTkEntry(self.form_container)
        self.age_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # MMSE Test Score
        ctk.CTkLabel(self.form_container, text="MMSE Test Score:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.mmse_entry = ctk.CTkEntry(self.form_container)
        self.mmse_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        #self.mmse_test_btn = ctk.CTkButton(self.button_frame, text="Start MMSE Test", width=150,
        #              command=self.launch_mmse_test)
        #self.mmse_test_btn.pack(side="left", padx=10)

        
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
                                        values=["Yes", "No"],
                                        variable=self.alcohol_var)
        self.alcohol_menu.grid(row=6, column=1, padx=10, pady=10, sticky="w")
        
        # Physical Activity
        ctk.CTkLabel(self.form_container, text="Physical Activity:").grid(row=7, column=0, padx=10, pady=10, sticky="e")
        self.activity_var = ctk.StringVar(value="Select")
        self.activity_menu = ctk.CTkOptionMenu(self.form_container, 
                                         values=["Low", "Moderate", "High"],
                                         variable=self.activity_var)
        self.activity_menu.grid(row=7, column=1, padx=10, pady=10, sticky="w")
        
        # Sleep Hours
        ctk.CTkLabel(self.form_container, text="Sleep Hours:").grid(row=8, column=0, padx=10, pady=10, sticky="e")
        self.sleep_entry = ctk.CTkEntry(self.form_container)
        self.sleep_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.button_frame.pack(pady=20)

        #self.mmse_test_btn = ctk.CTkButton(self.button_frame, text="Start MMSE Test", width=150,
        #              command=self.launch_mmse_test)
        #self.mmse_test_btn.pack(side="left", padx=10)

        
        self.clear_btn = ctk.CTkButton(self.button_frame, text="Clear", width=150, fg_color="#f0ad4e",
                      command=self.clear_fields)
        self.clear_btn.pack(side="left", padx=10)
        
        self.submit_btn = ctk.CTkButton(self.button_frame, text="Submit", width=150,
                      command=self.submit_data)
        self.submit_btn.pack(side="left", padx=10)
        
        self.predict_btn = ctk.CTkButton(self.button_frame, text="Predict Diagnosis", width=150,
                      command=self.predict_dementia)
        self.predict_btn.pack(side="left", padx=10)
        
        self.back_btn = ctk.CTkButton(self.button_frame, text="Back", width=150, fg_color="#d9534f",
                      command=lambda: self.controller.show_frame(SecondPage))
        self.back_btn.pack(side="left", padx=10)

    def launch_mmse_test(self):
        import subprocess
        subprocess.Popen(["python", "mmse_test_gui.py"])

    
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
            alcohol = 1 if self.alcohol_var.get() == "Yes" else 0
            activity = {"Low": 0, "Moderate": 1, "High": 2}[self.activity_var.get()]

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

        try:
            # Make prediction using loaded model
            prediction = self.controller.model.predict(user_data)[0]
            print("🎯 Prediction result:", prediction)

            # Save prediction to medical_history table
            conn = get_db_connection()
            cursor = conn.cursor()

            # Get patient_id using current user ID
            cursor.execute("SELECT patient_id FROM patients WHERE user_id=%s", 
                        (self.controller.current_user_id,))
            result = cursor.fetchone()

            if result:
                patient_id = result[0]
                cursor.execute(
                    "INSERT INTO medical_history (patient_id, diagnosis) VALUES (%s, %s)",
                    (patient_id, prediction)
                )
                conn.commit()
                conn.close()
            else:
                messagebox.showerror("Error", "Patient record not found. Please submit your data.")
                return

            # Store prediction in controller so ResultPage can access it
            self.controller.latest_prediction = prediction
            self.controller.show_frame(ResultPage)

        except Exception as e:
            print("🔥 Error during prediction:", e)
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")

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
    
    def on_resize(self, event):
        super().on_resize(event)
        width = self.winfo_width() if event is None else event.width
        height = self.winfo_height() if event is None else event.height
        
        # Adjust form field sizes
        if width < 800 or height < 600:
            # Smaller window - adjust form layout
            for entry in [self.age_entry, self.mmse_entry, self.weight_entry, 
                         self.height_entry, self.sleep_entry]:
                entry.configure(width=150)
            
            # Adjust button sizes and layout
            btn_width = min(120, (width-50)//4)
            self.clear_btn.configure(width=btn_width)
            self.submit_btn.configure(width=btn_width)
            self.predict_btn.configure(width=btn_width)
            self.back_btn.configure(width=btn_width)
            
            # Stack buttons vertically if needed
            if width < 600:
                self.clear_btn.pack_forget()
                self.submit_btn.pack_forget()
                self.predict_btn.pack_forget()
                self.back_btn.pack_forget()
                
                self.clear_btn.pack(pady=5)
                self.submit_btn.pack(pady=5)
                self.predict_btn.pack(pady=5)
                self.back_btn.pack(pady=5)
            else:
                # Ensure horizontal layout
                self.clear_btn.pack_forget()
                self.submit_btn.pack_forget()
                self.predict_btn.pack_forget()
                self.back_btn.pack_forget()
                
                self.clear_btn.pack(side="left", padx=5)
                self.submit_btn.pack(side="left", padx=5)
                self.predict_btn.pack(side="left", padx=5)
                self.back_btn.pack(side="left", padx=5)
        else:
            # Larger window - reset to defaults
            for entry in [self.age_entry, self.mmse_entry, self.weight_entry, 
                         self.height_entry, self.sleep_entry]:
                entry.configure(width=200)
            
            self.clear_btn.configure(width=150)
            self.submit_btn.configure(width=150)
            self.predict_btn.configure(width=150)
            self.back_btn.configure(width=150)
            
            # Ensure horizontal layout
            self.clear_btn.pack_forget()
            self.submit_btn.pack_forget()
            self.predict_btn.pack_forget()
            self.back_btn.pack_forget()
            
            self.clear_btn.pack(side="left", padx=10)
            self.submit_btn.pack(side="left", padx=10)
            self.predict_btn.pack(side="left", padx=10)
            self.back_btn.pack(side="left", padx=10)

# ------------------ Result Page ------------------
class ResultPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        
        self.result_data = None
        
        # Main container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Will be populated by display_results
        self.result_title = None
        self.info_frame = None
        self.diagnosis_frame = None
        self.suggestions_frame = None
        self.button_frame = None
    
    def display_results(self, result_data):
        self.result_data = result_data
        
        # Clear previous widgets
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Results title
        self.result_title = ctk.CTkLabel(self.container, 
                    text="Diagnosis Results",
                    font=ctk.CTkFont(size=24, weight="bold"))
        self.result_title.pack(pady=20)
        
        # Patient information frame
        self.info_frame = ctk.CTkFrame(self.container)
        self.info_frame.pack(pady=10, padx=20, fill="x")
        
        # Display patient info
        ctk.CTkLabel(self.info_frame, 
                    text=f"Patient: {result_data['username']}",
                    font=ctk.CTkFont(size=16)).pack(anchor="w", pady=5)
        
        ctk.CTkLabel(self.info_frame, 
                    text=f"Age: {result_data['age']} | Gender: {result_data['gender']}",
                    font=ctk.CTkFont(size=14)).pack(anchor="w", pady=5)
        
        # Diagnosis frame
        self.diagnosis_frame = ctk.CTkFrame(self.container)
        self.diagnosis_frame.pack(pady=20, padx=20, fill="x")
        
        # Diagnosis result with color coding
        if "High" in result_data['diagnosis']:
            diagnosis_color = "#d9534f"  # Red for high risk
        else:
            diagnosis_color = "#5cb85c"  # Green for low risk
            
        ctk.CTkLabel(self.diagnosis_frame, 
                    text=f"Diagnosis: {result_data['diagnosis']}",
                    font=ctk.CTkFont(size=18, weight="bold"),
                    text_color=diagnosis_color).pack(pady=10)
        
        ctk.CTkLabel(self.diagnosis_frame, 
                    text=f"Probability: {result_data['probability']}",
                    font=ctk.CTkFont(size=16)).pack(pady=5)
        
        # Suggestions frame
        self.suggestions_frame = ctk.CTkFrame(self.container)
        self.suggestions_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(self.suggestions_frame, 
                    text="Recommendations:",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.suggestions_text = ctk.CTkTextbox(self.suggestions_frame, 
                                        width=600, 
                                        height=200,
                                        font=ctk.CTkFont(size=14),
                                        wrap="word")
        self.suggestions_text.insert("1.0", result_data['suggestions'])
        self.suggestions_text.configure(state="disabled")
        self.suggestions_text.pack(pady=10)
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.button_frame.pack(pady=20)
        
        self.history_btn = ctk.CTkButton(self.button_frame, text="View History", width=150,
                     command=lambda: self.controller.show_frame(HistoryPage))
        self.history_btn.pack(side="left", padx=10)
        
        self.logout_btn = ctk.CTkButton(self.button_frame, text="Logout", width=150, fg_color="#d9534f",
                                          command=lambda: self.controller.show_frame(LoginPage))
        self.logout_btn.pack(side="left", padx=10)
        
        self.back_btn = ctk.CTkButton(self.button_frame, text="Back to Tests", width=150,
                     command=lambda: self.controller.show_frame(MedicalTestsPage))
        self.back_btn.pack(side="left", padx=10)
    
    def on_resize(self, event):
        super().on_resize(event)
        width = self.winfo_width() if event is None else event.width
        height = self.winfo_height() if event is None else event.height
        
        # Adjust textbox and button sizes
        if width < 800 or height < 600:
            # Smaller window
            if hasattr(self, 'suggestions_text'):
                self.suggestions_text.configure(width=width-100, height=height//3)
            
            # Adjust button sizes and layout
            btn_width = min(120, (width-50)//3)
            if hasattr(self, 'history_btn'):
                self.history_btn.configure(width=btn_width)
                self.logout_btn.configure(width=btn_width)
                self.back_btn.configure(width=btn_width)
                
                # Stack buttons vertically if needed
                if width < 500:
                    self.history_btn.pack_forget()
                    self.logout_btn.pack_forget()
                    self.back_btn.pack_forget()
                    
                    self.history_btn.pack(pady=5)
                    self.logout_btn.pack(pady=5)
                    self.back_btn.pack(pady=5)
                else:
                    # Ensure horizontal layout
                    self.history_btn.pack_forget()
                    self.logout_btn.pack_forget()
                    self.back_btn.pack_forget()
                    
                    self.history_btn.pack(side="left", padx=5)
                    self.logout_btn.pack(side="left", padx=5)
                    self.back_btn.pack(side="left", padx=5)
        else:
            # Larger window - reset to defaults
            if hasattr(self, 'suggestions_text'):
                self.suggestions_text.configure(width=600, height=200)
            
            if hasattr(self, 'history_btn'):
                self.history_btn.configure(width=150)
                self.logout_btn.configure(width=150)
                self.back_btn.configure(width=150)
                
                # Ensure horizontal layout
                self.history_btn.pack_forget()
                self.logout_btn.pack_forget()
                self.back_btn.pack_forget()
                
                self.history_btn.pack(side="left", padx=10)
                self.logout_btn.pack(side="left", padx=10)
                self.back_btn.pack(side="left", padx=10)

        self.label = ctk.CTkLabel(self, text="Diagnosis Result Will Appear Here", font=("Arial", 20))
        self.label.pack(pady=50)

        self.back_btn = ctk.CTkButton(self, text="Back to Home",
                                      command=lambda: controller.show_frame(MedicalTestsPage))
        self.back_btn.pack(pady=10)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        prediction = self.controller.latest_prediction
        self.label.configure(text=f"Prediction: {prediction}")


# ------------------ History Page ------------------
class HistoryPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="both", expand=True)
        
        self.title_label = ctk.CTkLabel(self.container, 
                     text="Medical History",
                     font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=20)
        
        # Treeview for displaying history
        self.tree_frame = ctk.CTkFrame(self.container)
        self.tree_frame.pack(fill="both", expand=True, pady=10)
        
        # Scrollbar
        self.tree_scroll = ctk.CTkScrollbar(self.tree_frame)
        self.tree_scroll.pack(side="right", fill="y")
        
        # Create Treeview
        self.history_tree = ttk.Treeview(self.tree_frame, 
                                      yscrollcommand=self.tree_scroll.set,
                                      selectmode="extended")
        self.history_tree.pack(fill="both", expand=True)
        
        # Configure scrollbar
        self.tree_scroll.configure(command=self.history_tree.yview)
        
        # Define columns
        self.history_tree['columns'] = ("Date", "Diagnosis", "Probability", "Notes")
        
        # Format columns
        self.history_tree.column("#0", width=0, stretch=False)
        self.history_tree.column("Date", anchor="center", width=100)
        self.history_tree.column("Diagnosis", anchor="center", width=100)
        self.history_tree.column("Probability", anchor="center", width=100)
        self.history_tree.column("Notes", anchor="w", width=300)
        
        # Create headings
        self.history_tree.heading("#0", text="", anchor="w")
        self.history_tree.heading("Date", text="Date", anchor="center")
        self.history_tree.heading("Diagnosis", text="Diagnosis", anchor="center")
        self.history_tree.heading("Probability", text="Probability", anchor="center")
        self.history_tree.heading("Notes", text="Notes", anchor="w")
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self.container, fg_color="transparent")
        self.button_frame.pack(pady=20)
        
        self.back_btn = ctk.CTkButton(self.button_frame, text="Back", width=150,
                     command=lambda: controller.show_frame(ResultPage))
        self.back_btn.pack(side="left", padx=10)
        
        self.refresh_btn = ctk.CTkButton(self.button_frame, text="Refresh", width=150,
                     command=self.load_history)
        self.refresh_btn.pack(side="left", padx=10)
        
        self.export_btn = ctk.CTkButton(self.button_frame, text="Export to CSV", width=150,
                     command=self.export_history)
        self.export_btn.pack(side="left", padx=10)
    
    def on_show(self):
        """Load history when page is shown"""
        self.load_history()
    
    def load_history(self):
        """Load patient history from database"""
        # Clear existing data
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        try:
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                
                # Get patient_id
                cursor.execute("SELECT patient_id FROM patients WHERE user_id=%s", 
                             (self.controller.current_user_id,))
                patient_id = cursor.fetchone()[0]
                
                # Get history
                cursor.execute("""
                    SELECT diagnosis_date, diagnosis, notes 
                    FROM medical_history 
                    WHERE patient_id=%s 
                    ORDER BY diagnosis_date DESC
                """, (patient_id,))
                
                # Add to treeview
                for row in cursor.fetchall():
                    date = row[0].strftime("%Y-%m-%d")
                    diagnosis = row[1]
                    
                    # Extract probability from notes if available
                    notes = row[2]
                    probability = "N/A"
                    if "probability:" in notes.lower():
                        try:
                            probability = notes.split("probability:")[1].strip().split()[0]
                        except:
                            pass
                    
                    self.history_tree.insert("", "end", 
                                          values=(date, diagnosis, probability, notes))
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn:
                conn.close()
    
    def export_history(self):
        """Export history to CSV file"""
        try:
            # Get all items from treeview
            items = self.history_tree.get_children()
            if not items:
                messagebox.showwarning("No Data", "No history records to export")
                return
                
            # Prepare data
            data = []
            for item in items:
                values = self.history_tree.item(item)['values']
                data.append(values)
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=["Date", "Diagnosis", "Probability", "Notes"])
            
            # Save to file
            filename = f"dementia_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            df.to_csv(filename, index=False)
            
            messagebox.showinfo("Success", f"History exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))
    
    def on_resize(self, event):
        super().on_resize(event)
        width = self.winfo_width() if event is None else event.width
        height = self.winfo_height() if event is None else event.height
        
        # Adjust treeview column widths
        if hasattr(self, 'history_tree'):
            if width < 800 or height < 600:
                # Smaller window
                self.history_tree.column("Date", width=80)
                self.history_tree.column("Diagnosis", width=80)
                self.history_tree.column("Probability", width=80)
                self.history_tree.column("Notes", width=min(300, width-300))
                
                # Adjust button sizes
                btn_width = min(120, (width-50)//3)
                self.back_btn.configure(width=btn_width)
                self.refresh_btn.configure(width=btn_width)
                self.export_btn.configure(width=btn_width)
                
                # Stack buttons vertically if needed
                if width < 500:
                    self.back_btn.pack_forget()
                    self.refresh_btn.pack_forget()
                    self.export_btn.pack_forget()
                    
                    self.back_btn.pack(pady=5)
                    self.refresh_btn.pack(pady=5)
                    self.export_btn.pack(pady=5)
                else:
                    # Ensure horizontal layout
                    self.back_btn.pack_forget()
                    self.refresh_btn.pack_forget()
                    self.export_btn.pack_forget()
                    
                    self.back_btn.pack(side="left", padx=5)
                    self.refresh_btn.pack(side="left", padx=5)
                    self.export_btn.pack(side="left", padx=5)
            else:
                # Larger window - reset to defaults
                self.history_tree.column("Date", width=100)
                self.history_tree.column("Diagnosis", width=100)
                self.history_tree.column("Probability", width=100)
                self.history_tree.column("Notes", width=300)
                
                self.back_btn.configure(width=150)
                self.refresh_btn.configure(width=150)
                self.export_btn.configure(width=150)
                
                # Ensure horizontal layout
                self.back_btn.pack_forget()
                self.refresh_btn.pack_forget()
                self.export_btn.pack_forget()
                
                self.back_btn.pack(side="left", padx=10)
                self.refresh_btn.pack(side="left", padx=10)
                self.export_btn.pack(side="left", padx=10)

# ------------------ Run Application ------------------
if __name__ == "__main__":
    app = DementiaApp()
    app.mainloop()