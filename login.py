import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re
from hashlib import sha256

# Connect to MySQL database
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pooji",
        database="dementia_db"
    )

# Hash password for storing securely
def hash_password(password):
    return sha256(password.encode()).hexdigest()

# Validate username and password (simple example)
def validate_registration(username, password):
    if len(username) < 4:
        return "Username must be at least 4 characters."
    if len(password) < 6:
        return "Password must be at least 6 characters."
    if not re.search(r"[A-Za-z]", password) or not re.search(r"\d", password):
        return "Password must contain both letters and numbers."
    return None

# Registration page
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Register", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Register", command=self.register_user).pack(pady=10)
        tk.Button(self, text="Go to Login", command=lambda: controller.show_frame(LoginPage)).pack()

    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        error = validate_registration(username, password)
        if error:
            messagebox.showerror("Error", error)
            return

        hashed_pw = hash_password(password)

        try:
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            db.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.controller.show_frame(LoginPage)
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            db.close()

# Login page
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self, text="Username").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login_user).pack(pady=10)
        tk.Button(self, text="Go to Register", command=lambda: controller.show_frame(RegisterPage)).pack()

    def login_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        hashed_pw = hash_password(password)

        try:
            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, hashed_pw))
            user = cursor.fetchone()

            if user:
                self.controller.user_id = user['id']
                messagebox.showinfo("Success", f"Welcome {username}!")
                self.controller.show_frame(DementiaFormPage)
            else:
                messagebox.showerror("Error", "Invalid username or password.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            db.close()


class DementiaFormPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Fill Dementia Prediction Details", font=("Arial", 16)).pack(pady=10)

        # Age - Entry
        tk.Label(self, text="Age").pack()
        self.age_entry = tk.Entry(self)
        self.age_entry.pack()

        # Gender - Radio Buttons
        tk.Label(self, text="Gender").pack()
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = tk.Frame(self)
        gender_frame.pack()
        for gender in ["Male", "Female"]:
            tk.Radiobutton(gender_frame, text=gender, variable=self.gender_var, value=gender).pack(side="left")

        # Smoking Status - Radio Buttons
        tk.Label(self, text="Smoking Status").pack()
        self.smoking_var = tk.StringVar(value="No")
        smoking_frame = tk.Frame(self)
        smoking_frame.pack()
        for status in ["Yes", "No"]:
            tk.Radiobutton(smoking_frame, text=status, variable=self.smoking_var, value=status).pack(side="left")

        # Physical Activity - Radio Buttons
        tk.Label(self, text="Physical Activity").pack()
        self.physical_var = tk.StringVar(value="Medium")
        physical_frame = tk.Frame(self)
        physical_frame.pack()
        for level in ["Low", "Medium", "High"]:
            tk.Radiobutton(physical_frame, text=level, variable=self.physical_var, value=level).pack(side="left")

        # Cognitive Test Scores - Entry
        tk.Label(self, text="Cognitive Test Scores (0-100)").pack()
        self.cognitive_entry = tk.Entry(self)
        self.cognitive_entry.pack()

        # Sleep Quality - Radio Buttons
        tk.Label(self, text="Sleep Quality").pack()
        self.sleep_var = tk.StringVar(value="Good")
        sleep_frame = tk.Frame(self)
        sleep_frame.pack()
        for quality in ["Poor", "Good", "Excellent"]:
            tk.Radiobutton(sleep_frame, text=quality, variable=self.sleep_var, value=quality).pack(side="left")

        # Nutrition Diet - Radio Buttons
        tk.Label(self, text="Nutrition Diet").pack()
        self.nutrition_var = tk.StringVar(value="Good")
        nutrition_frame = tk.Frame(self)
        nutrition_frame.pack()
        for diet in ["Poor", "Good", "Excellent"]:
            tk.Radiobutton(nutrition_frame, text=diet, variable=self.nutrition_var, value=diet).pack(side="left")

        # Depression Status - Radio Buttons
        tk.Label(self, text="Depression Status").pack()
        self.depression_var = tk.StringVar(value="No")
        depression_frame = tk.Frame(self)
        depression_frame.pack()
        for status in ["Yes", "No"]:
            tk.Radiobutton(depression_frame, text=status, variable=self.depression_var, value=status).pack(side="left")

        # Family History - Radio Buttons
        tk.Label(self, text="Family History").pack()
        self.family_var = tk.StringVar(value="No")
        family_frame = tk.Frame(self)
        family_frame.pack()
        for history in ["Yes", "No"]:
            tk.Radiobutton(family_frame, text=history, variable=self.family_var, value=history).pack(side="left")

        tk.Button(self, text="Submit", command=self.submit_details).pack(pady=10)
        tk.Button(self, text="Logout", command=self.logout).pack()

    def submit_details(self):
        try:
            age = int(self.age_entry.get())
            gender = self.gender_var.get()
            smoking = self.smoking_var.get()
            physical = self.physical_var.get()
            cognitive = float(self.cognitive_entry.get())
            sleep = self.sleep_var.get()
            nutrition = self.nutrition_var.get()
            depression = self.depression_var.get()
            family = self.family_var.get()

            if not (0 <= cognitive <= 100):
                raise ValueError("Cognitive Test Scores must be between 0 and 100")
            if age < 0:
                raise ValueError("Age must be positive")

            # Store data in DB (same as before)
            db = get_db_connection()
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO user_details (
                    user_id, age, gender, smoking_status, physical_activity,
                    cognitive_test_scores, sleep_quality, nutrition_diet,
                    depression_status, family_history
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                self.controller.user_id, age, gender, smoking, physical,
                cognitive, sleep, nutrition, depression, family
            ))
            db.commit()

            messagebox.showinfo("Success", "Details saved successfully! Prediction logic can be added here.")

        except ValueError as ve:
            messagebox.showerror("Validation Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            db.close()

    def logout(self):
        self.controller.user_id = None
        self.controller.show_frame(LoginPage)


# Main app class
class DementiaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dementia Detection App")
        self.geometry("400x600")
        self.user_id = None

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginPage, RegisterPage, DementiaFormPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()


if __name__ == "__main__":
    app = DementiaApp()
    app.mainloop()
