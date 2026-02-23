import tkinter as tk
from tkinter import messagebox,ttk,font
import mysql.connector
from PIL import Image, ImageTk  # To display logos
import pandas as pd
import joblib

# ------------------ MySQL Config ------------------
def insert_user(name, email, username, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pooji",
            database="dementia_app"
        )
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)",
                       (name, email, username, password))
        conn.commit()
        conn.close()
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("MySQL Error", str(err))
        return False

# ------------------ Main Application ------------------
class DementiaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Initial Diagnosis of Dementia")
        self.attributes("-fullscreen", True)  # Enable full-screen mode
        self.configure(bg="#d0e7f9")

        self.frames = {}
        for F in (MainPage, SecondPage, AbstractPage, AlgorithmPage, LoginPage, RegisterPage, MedicalTestsPage,ResultPage):
            page = F(parent=self, controller=self)
            self.frames[F] = page
            page.place(relwidth=1, relheight=1)

        self.show_frame(MainPage)

        # Allow users to exit full-screen mode
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))

    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
# ------------------ Pages ------------------
'''class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#d0e7f9")
        self.controller = controller
        tk.Label(self, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                 font=("Times New Roman", 16, "bold"), bg="#d0e7f9").pack(pady=10)'''

import tkinter as tk

class BasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#d0e7f9")
        self.controller = controller
        
        # Title label common to all pages
        self.title_font = ("Times New Roman", 16, "bold")
        self.title_label = tk.Label(
            self,
            text="Initial Diagnosis of Dementia using Machine Learning Approach",
            font=self.title_font,
            bg="#d0e7f9"
        )
        self.title_label.pack(pady=10)
        
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#d0e7f9")
        self.controller = controller

        # Container with less padding to reduce blue borders

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container = tk.Frame(self, bg="white", padx=10, pady=10)
        container.pack(padx=40, pady=20, fill="both", expand=True)

        # Logo section
        top_frame = tk.Frame(container, bg="white")
        top_frame.pack(fill="x")

        # Left logo
        left_logo = Image.open("gvp logo.png").resize((100,100))  # Adjust size as needed
        self.left_logo_img = ImageTk.PhotoImage(left_logo)
        tk.Label(top_frame, image=self.left_logo_img, bg="white").pack(side="left", padx=10)

        # Center labels
        title_frame = tk.Frame(top_frame, bg="white")
        title_frame.pack(side="left", expand=True)
        tk.Label(title_frame, text="GAYATRI VIDYA PARISHAD", font=("courier", 22, "bold"), bg="white").pack()
        tk.Label(title_frame, text="COLLEGE FOR DEGREE AND PG COURSES (A)", font=("courier", 18), bg="white").pack()
        tk.Label(title_frame, text="Department of Computer Applications", font=("Times New Roman", 14,"bold"), bg="white").pack()

        # Right logo
        right_logo = Image.open("gvp logo.png").resize((100,100))
        self.right_logo_img = ImageTk.PhotoImage(right_logo)
        tk.Label(top_frame, image=self.right_logo_img, bg="white").pack(side="right", padx=10)

        # Project Title
        tk.Label(container, text="Initial Diagnosis of Dementia using Machine Learning Approach",
                 font=("Times New Roman", 20, "bold", "underline"), bg="white").pack(pady=20)

        # Author & Guide Info
        content = tk.Frame(container, bg="white")
        content.pack(pady=10)
        tk.Label(content, text="By: P. Poojitha \nPG232402030 \n Master of Computer Applications\nSem-IV", bg="white").pack(side="left", padx=40)
        tk.Label(content, text="Project guide:\nMrs. P. Ratna Pavani\nAssistant Professor\nDept of Computer Applications",
                 bg="white").pack(side="right", padx=40)
    # Buttons at bottom corners of the window
        bottom_frame = tk.Frame(self, bg="#d0e7f9")
        bottom_frame.pack(side="bottom", fill="x", pady=10)

        tk.Button(bottom_frame, text="Proceed", width=15, bg="#4CAF50", fg="white",
                  command=lambda: controller.show_frame(SecondPage)).pack(side="left", padx=20)

        tk.Button(bottom_frame, text="Exit", width=15, bg="#f44336", fg="white",
                  command=self.confirm_exit).pack(side="right", padx=20)

    def confirm_exit(self):
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            self.controller.destroy()  # Or controller.quit() depending on app structure
        

class SecondPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller
        
        # Root frame background
        self.configure(bg="#d0e7f9")
        
        # Main container: will hold left and right frames
        self.container = tk.Frame(self, bg="#d0e7f9")
        self.container.pack(fill="both", expand=True, padx=40, pady=30)
        
        # Left frame for image
        self.left_frame = tk.Frame(self.container, bg="#d0e7f9")
        self.left_frame.pack(side="left", fill="both", expand=True)
        
        # Right frame for buttons
        self.right_frame = tk.Frame(self.container, bg="#d0e7f9")
        self.right_frame.pack(side="left", fill="both", expand=True)
        
        # Load the image (replace 'dementia.jpeg' with actual image file path)
        try:
            img = Image.open("dementia.jpeg")
            # Resize image to fit initial size roughly, will rescale dynamically
            img = img.resize((400, 400), Image.ANTIALIAS)
            self.dementia_img = ImageTk.PhotoImage(img)
        except Exception:
            # If the image fails to load, use a placeholder label
            self.dementia_img = None
        
        if self.dementia_img:
            self.img_label = tk.Label(self.left_frame, image=self.dementia_img, bg="#ffffff")
        else:
            self.img_label = tk.Label(self.left_frame, text="[Image Placeholder]", font=("Poppins", 20, "bold"), bg="#d0e7f9", fg="#6b7280", padx=20, pady=20, relief="ridge", borderwidth=2)
        self.img_label.pack(expand=True)
        
        # Create icons as Unicode as placeholder, or use small image icons if available
        # Using Unicode emoji for simplicity here
        abstract_icon = "\u270D"  # ✍ Pencil
        algorithm_icon = "\u2699" # ⚙ Gear
        howto_icon = "\u2753"    # ❓ Question mark
        
        # Buttons container in the right frame
        self.buttons_container = tk.Frame(self.right_frame, bg="#d0e7f9")
        self.buttons_container.pack(expand=True)
        
        # Create buttons with text and icons
        self.abstract_btn = tk.Button(self.buttons_container,
                                      text=f"{abstract_icon}  Abstract",
                                      font=("Poppins", 16, "bold"),
                                      width=20, height=2,
                                      bg="#f0f0f0", fg="#333333",
                                      relief="raised", bd=2,
                                      command=lambda: controller.show_frame(AbstractPage))
        self.algorithm_btn = tk.Button(self.buttons_container,
                                      text=f"{algorithm_icon}  Algorithm & Example",
                                      font=("Poppins", 16, "bold"),
                                      width=20, height=2,
                                      bg="#f0f0f0", fg="#333333",
                                      relief="raised", bd=2,
                                      command=lambda: controller.show_frame(AlgorithmPage))
        self.howto_btn = tk.Button(self.buttons_container,
                                      text=f"{howto_icon}  How to Use",
                                      font=("Poppins", 16, "bold"),
                                      width=20, height=2,
                                      bg="#f0f0f0", fg="#333333",
                                      relief="raised", bd=2,
                                      command=lambda: messagebox.showinfo("Example", "Usage content"))
        
        # Pack buttons vertically initially
        self.abstract_btn.pack(pady=10)
        self.algorithm_btn.pack(pady=10)
        self.howto_btn.pack(pady=10)
        
        # Bottom frame for login and back buttons
        bottom_frame = tk.Frame(self, bg="#d0e7f9")
        bottom_frame.pack(side="bottom", fill="x", pady=10)

        tk.Button(bottom_frame, text="Login", width=20, height=2, bg="#4CAF50", fg="white",
                  command=lambda: controller.show_frame(LoginPage)).pack(side="right", padx=20)
        tk.Button(bottom_frame, text="Back", width=20, height=2, bg="#1E2DCC", fg="white",
                  command=lambda: controller.show_frame(MainPage)).pack(side="right", padx=20)

        
        # Bind window configure event to handle responsive layout
        self.bind("<Configure>", self._on_resize)
    
    def _on_resize(self, event):
        # Get current width and height of the frame
        width = event.width
        height = event.height
        
        # Threshold width for switching layout (e.g., 700 pixels)
        threshold_width = 700
        
        # Clear current button pack for rearrangement
        for widget in self.buttons_container.winfo_children():
            widget.pack_forget()
        
        # Container packing - clear then repack
        self.left_frame.pack_forget()
        self.right_frame.pack_forget()
        
        if width >= threshold_width:
            # Large window layout: horizontal split
            self.left_frame.pack(side="left", fill="both", expand=True, padx=(0,20))
            self.right_frame.pack(side="left", fill="both", expand=True)
            
            # Buttons stacked vertically
            self.abstract_btn.pack(pady=10)
            self.algorithm_btn.pack(pady=10)
            self.howto_btn.pack(pady=10)
        else:
            # Small window layout: vertical split
            self.left_frame.pack(side="top", fill="both", expand=True, pady=(0,20))
            self.right_frame.pack(side="top", fill="both", expand=True)
            
            # Buttons lined up horizontally side by side
            self.abstract_btn.pack(side="left", expand=True, padx=10, pady=0)
            self.algorithm_btn.pack(side="left", expand=True, padx=10, pady=0)
            self.howto_btn.pack(side="left", expand=True, padx=10, pady=0)
        
        # Optionally, resize the image dynamically to fit half container
        # Get the size of left_frame and resize image accordingly (only if image is present)
        if self.dementia_img:
            # Get current left frame size
            lf_width = self.left_frame.winfo_width() or 400
            lf_height = self.left_frame.winfo_height() or 400
            
            # Resize image while keeping aspect ratio
            try:
                img = Image.open("dementia.jpeg")
                img_ratio = img.width / img.height
                target_width = lf_width
                target_height = int(target_width / img_ratio)
                if target_height > lf_height:
                    target_height = lf_height
                    target_width = int(target_height * img_ratio)
                img = img.resize((target_width, target_height), Image.ANTIALIAS)
                self.dementia_img = ImageTk.PhotoImage(img)
                self.img_label.config(image=self.dementia_img)
            except Exception:
                pass


class AbstractPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Abstract", font=("Courier", 20, "underline"), bg="#d0e7f9").pack(pady=10)

        content = (
            "Dementia is a brain disorder that affects memory, thinking, and daily life.Early diagnosis is"
             "crucial for timely treatment and better patient care. Traditional methods like cognitive tests" 
             "and brain scans are often slow, expensive, and require medical experts, leading to delayed diagnosis." 
             "Some AI methods, such as SVM and k-NN, struggle with handling large datasets and achieving high accuracy." 
             "This project proposes using the Random Forest algorithm for early dementia detection. It analyzes patient" 
             "data, including memory test results, lifestyle, and medical history, to predict dementia risk efficiently."
             "Random Forest is effective in handling large medical datasets, avoiding overfitting, and providing high accuracy." 
             "The model offers a reliable, cost-effective, and automated solution for detecting dementia at an early stage."

        )
        tk.Message(self, text=content, bg="#d0e7f9", width=800, font=("Arial", 12)).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: controller.show_frame(SecondPage), bg="#f44336", fg="white").pack(pady=10)

class AlgorithmPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Algorithm", font=("Courier", 20, "underline"), bg="#d0e7f9").pack(pady=10)

        content = (
            "Random Forest Algorithm"
            "The Random Forest algorithm is a powerful AI algorithm that uses many decision trees to make better predictions.\n"
            "By combining the results of multiple trees, it improves accuracy and reduces mistakes.It is used for handling large\n"
            "data and works well for early predictions. It can handle and analyze different types of patient data, like memory test\n"
            "scores, lifestyle, and medical history, to predict dementia risk.\n"
            "1: Data Collection \n"
            "2: Data Preprocessing\n"
            "3: Model Selection\n"
            "4: Model Training\n"
            "5: Model Optimization\n"
            "6: Model Evaluation\n"
            "7: Deployment"
        )
        tk.Message(self, text=content, bg="#d0e7f9", width=800, font=("Arial", 12)).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: controller.show_frame(SecondPage), bg="#f44336", fg="white").pack(pady=10)

class LoginPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Login", font=("Arial", 14), bg="#d0e7f9").pack(pady=10)

        self.username = tk.Entry(self)
        self.password = tk.Entry(self, show="*")

        tk.Label(self, text="Username", bg="#d0e7f9").pack()
        self.username.pack()
        tk.Label(self, text="Password", bg="#d0e7f9").pack()
        self.password.pack()

        tk.Button(self, text="Login", width=15, bg="#4CAF50", fg="white", command=self.check_login).pack(pady=5)
        tk.Button(self, text="New User? Register", width=15, bg="#2196F3", fg="white",
                  command=lambda: controller.show_frame(RegisterPage)).pack(pady=5)
        tk.Button(self, text="Back", width=15, command=lambda: controller.show_frame(SecondPage)).pack(pady=5)

    def check_login(self):
        uname = self.username.get()
        pwd = self.password.get()
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pooji",
                database="dementia_app"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (uname, pwd))
            if cursor.fetchone():
                messagebox.showinfo("Login Success", f"Welcome {uname}!")
                self.controller.frames[MedicalTestsPage].set_username(uname)
                self.controller.show_frame(MedicalTestsPage)
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

class RegisterPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Register New User", font=("Arial", 14), bg="#d0e7f9").pack(pady=10)

        self.entries = {}
        for field in ["Name", "Email", "Username", "Password", "Confirm Password"]:
            tk.Label(self, text=field, bg="#d0e7f9").pack()
            entry = tk.Entry(self, show="*" if "Password" in field else None)
            entry.pack()
            self.entries[field] = entry

        tk.Button(self, text="Register", width=15, bg="#4CAF50", fg="white", command=self.register_user).pack(pady=10)
        tk.Button(self, text="Back", width=15, command=lambda: controller.show_frame(LoginPage)).pack()

    def register_user(self):
        def register_user(self):
            data = {key: ent.get().strip() for key, ent in self.entries.items()}
            if not all(data.values()):
                messagebox.showerror("Error", "Please fill all fields")
                return
        
            if data["Password"] != data["Confirm Password"]:
                messagebox.showerror("Error", "Password and Confirm Password do not match!")
                return
        
        # Insert user without confirm_password saved
            if insert_user(data["Name"], data["Email"], data["Username"], data["Password"]):
                messagebox.showinfo("Success", "Registered successfully!")
                self.controller.show_frame(LoginPage)



# Load trained model & features
model = joblib.load("dementia_model.pkl")
feature_columns = joblib.load("model_features.pkl")

class MedicalTestsPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        container = tk.Frame(self, bg="#f9fafb", padx=30, pady=30, bd=1, relief="solid")
        container.pack(padx=50, pady=40)
        tk.Label(container, text="Medical Tests", font=("Inter", 24, "bold"), fg="#111111", bg="#f9fafb").pack(pady=(0,20))
        self.username_label = tk.Label(container, text="", font=("Inter", 14), bg="#f9fafb", fg="#4b5563")
        self.username_label.pack(pady=(0, 20))


        # Gender
        tk.Label(self, text="Gender:", bg="#d0e7f9").pack()
        self.gender_var = tk.StringVar(value="Select")
        tk.OptionMenu(self, self.gender_var, "Male", "Female").pack()

        # Age
        tk.Label(self, text="Age:", bg="#d0e7f9").pack()
        self.age_entry = tk.Entry(self)
        self.age_entry.pack()

        # MMSE Test Score
        tk.Label(self, text="MMSE Test Score:", bg="#d0e7f9").pack()
        self.mmse_entry = tk.Entry(self)
        self.mmse_entry.pack()

        # BMI Calculation
        tk.Label(self, text="Weight (kg):", bg="#d0e7f9").pack()
        self.weight_entry = tk.Entry(self)
        self.weight_entry.pack()

        tk.Label(self, text="Height (cm):", bg="#d0e7f9").pack()
        self.height_entry = tk.Entry(self)
        self.height_entry.pack()

        # Smoking
        tk.Label(self, text="Smoking:", bg="#d0e7f9").pack()
        self.smoking_var = tk.StringVar(value="Select")
        tk.OptionMenu(self, self.smoking_var, "Yes", "No").pack()

        # Alcohol Consumption
        tk.Label(self, text="Alcohol Consumption:", bg="#d0e7f9").pack()
        self.alcohol_var = tk.StringVar(value="Select")
        tk.OptionMenu(self, self.alcohol_var, "Yes", "No").pack()

        # Physical Activity
        tk.Label(self, text="Physical Activity Level:", bg="#d0e7f9").pack()
        self.activity_var = tk.StringVar(value="Select")
        tk.OptionMenu(self, self.activity_var, "Low", "Moderate", "High").pack()

        # Sleep Hours
        tk.Label(self, text="Sleep Hours:", bg="#d0e7f9").pack()
        self.sleep_entry = tk.Entry(self)
        self.sleep_entry.pack()

        button_frame = tk.Frame(self, bg="#d0e7f9")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Clear", width=15, bg="#ff9800", fg="white", command=self.clear_fields).pack(side="left", padx=5)
        tk.Button(button_frame, text="Submit", width=15, bg="#4CAF50", fg="white", command=self.submit_data).pack(side="right", padx=5)
        tk.Button(self, text="Predict Diagnosis", width=15, bg="#4CAF50", fg="white", command=self.predict_dementia).pack(pady=5)
        tk.Button(self, text="Back", width=15, bg="#2196F3", fg="white", command=lambda: controller.show_frame(ResultPage)).pack(pady=10)

    def set_username(self, uname):
        self.username_label.config(text=f"Welcome {uname}! Let's Get Started.")
    
    def clear_fields(self):
        for entry in [self.age_entry, self.mmse_entry, self.weight_entry, self.height_entry, self.sleep_entry]:
            entry.delete(0, tk.END)

    def submit_data(self):
        messagebox.showinfo("Submission", "Data successfully submitted!")

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  # Convert cm to meters
            bmi=(weight / (height ** 2), 2)
            return bmi
        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height values.")
            return None

    def get_user_inputs(self):
        try:
            age = int(self.age_entry.get())
            gender = 1 if self.gender_var.get() == "Male" else 0
            mmse_score = int(self.mmse_entry.get())
            bmi = self.calculate_bmi()
            smoking = 1 if self.smoking_var.get() == "Yes" else 0
            alcohol = 1 if self.alcohol_var.get() == "Yes" else 0
            activity = {"Low": 0, "Moderate": 1, "High": 2}[self.activity_var.get()]
            sleep_hours = float(self.sleep_entry.get())

            if bmi is None:
                return None

            # Convert input to DataFrame & match trained model's features
            user_data = pd.DataFrame([[gender, age, mmse_score, bmi, smoking, alcohol, activity, sleep_hours]], columns=feature_columns)
            return user_data
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values.")
            return None

    def predict_dementia(self):
        user_data = self.get_user_inputs()
        if user_data is not None:
            prediction = model.predict(user_data)

            if prediction[0] == 1:
                messagebox.showinfo("Diagnosis Result", "High Risk of Dementia. Please consult a doctor.")
            else:
                messagebox.showinfo("Diagnosis Result", "Low Risk of Dementia.")

class ResultPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        tk.Label(self, text="Abstract", font=("Courier", 20, "underline"), bg="#d0e7f9").pack(pady=10)

        content = (
            "Result of the analysis"

        )
        tk.Message(self, text=content, bg="#d0e7f9", width=800, font=("Arial", 12)).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: controller.show_frame(SecondPage), bg="#f44336", fg="white").pack(pady=10)

# ------------------ Run App ------------------
if __name__ == "__main__":
    app = DementiaApp()
    app.mainloop()
