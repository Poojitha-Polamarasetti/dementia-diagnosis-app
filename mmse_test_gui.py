import tkinter as tk
from tkinter import messagebox, PhotoImage, scrolledtext
import datetime
import random
import os
import tempfile


from PIL import Image, ImageTk  # Required if using .jpg or to support more formats

class MMSETestApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MMSE Test")
        self.geometry("700x700")

        # ✅ Main content frame on top of background
        self.container = tk.Frame(self, bg="#aedef8")
        self.container.pack(fill="both", expand=True)

        # Ensure stacking order
        if hasattr(self, 'bg_label'):
            self.bg_label.lower()
            self.container.lift()

        # === MMSE Logic ===
        self.score = 0
        self.current_question = 0
        self.responses = []
        self.word_list = ["ball", "flag", "tree"]

        self.questions = self.create_questions()
        self.show_question()

    def create_questions(self):
        today = datetime.datetime.now()
        month = today.month
        season = "summer"
        if month in [3, 4, 5]:
            season = "summer"
        elif month in [6, 7, 8]:
            season = "monsoon"
        elif month in [9, 10, 11]:
            season = "autumn"
        else:
            season = "winter"

        return [
            {"type": "entry", "question": "What is today's date?", "answer": str(today.day)},
            {"type": "entry", "question": "What day of the week is it?", "answer": today.strftime("%A").lower()},
            {"type": "entry", "question": "What month is it?", "answer": today.strftime("%B").lower()},
            {"type": "entry", "question": "What year is it?", "answer": str(today.year)},
            {"type": "radio", "question": "Where are you right now?", "options": ["home", "hospital", "school", "park"], "answer": "home"},
            {"type": "info", "question": "Memorize these 3 words: Ball, Flag, Tree. Click Next when ready."},
            {"type": "recall_words", "question": "Recall the 3 words shown earlier.", "answer": ["ball", "flag", "tree"]},
            {"type": "serial7s", "question": "Subtract 7 from 100 and keep subtracting 7 five times. (Enter 5 numbers separated by space)", "answer": ["93", "86", "79", "72", "65"]},
            {"type": "entry", "question": "Repeat the phrase exactly: 'No ifs, ands, or buts.'", "answer": "no ifs, ands, or buts."},
            {"type": "entry", "question": "Write a meaningful sentence.", "custom_eval": self.evaluate_sentence},
            {"type": "button", "question": "Read and follow this: Close your eyes. Click 'Done' after 5 seconds.", "answer": "done"},
            {"type": "checkbox", "question": "Select the actions after performing it: Pick up paper, Fold it, Place it on floor", "options": ["Pick up paper", "Fold it", "Place it on floor"], "answer": ["Pick up paper", "Fold it", "Place it on floor"]},
            {"type": "image_radio", "question": "Name the object shown in the image.", "image": "images/img1.png", "options": ["pen", "apple", "clock", "bottle"], "answer": "clock"},
            {"type": "image_radio", "question": "What object was shown earlier?", "image": "images/img2.png", "options": ["ball", "tree", "hat", "box"], "answer": "tree"},
            {"type": "mcq", "question": "What comes next: 2, 4, 6, 8, ?", "options": ["9", "10", "11", "12"], "answer": "10"},
            {"type": "mcq", "question": "In which direction does the sun rise?", "options": ["North", "East", "South", "West"], "answer": "east"},
            {"type": "image_radio", "question": "What color was the circle in the image?", "image": "images/img3.png", "options": ["red", "green", "blue", "yellow"], "answer": "blue"},
            {"type": "image_radio", "question": "Where was the square positioned?", "image": "images/img4.png", "options": ["Top-left", "Center", "Bottom-right", "Top-right"], "answer": "bottom-right"},
            {"type": "mcq", "question": "Which is grammatically correct?", "options": ["He go to school", "He goes to school", "He going school", "He gone to school"], "answer": "he goes to school"},
            {"type": "mcq", "question": "If you have 3 apples and give 1 away, how many are left?", "options": ["1", "2", "3", "4"], "answer": "2"},
            {"type": "entry_disappear", "question": "Spell the word backwards.", "answer": "dlrow"},
            {"type": "mcq", "question": "What season is it now?", "options": ["summer", "monsoon", "autumn", "winter"], "answer": season},
            {"type": "image_radio", "question": "Which direction was the arrow pointing in the image?", "image": "images/img5.png", "options": ["left", "right", "up", "down"], "answer": "right"}
        ]

    def show_question(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        if self.current_question >= len(self.questions):
            self.finish_test()
            return

        q = self.questions[self.current_question]
        tk.Label(self.container, text=f"Q{self.current_question+1}: {q['question']}", 
                 font=("Arial", 16), wraplength=600, bg="#aedef8").pack(pady=60)

        self.user_input = None
        self.var = None

        if q["type"] == "entry":
            self.user_input = tk.Entry(self.container, font=("Arial", 14))
            self.user_input.pack(pady=10)

        elif q["type"] == "entry_disappear":
            label = tk.Label(self.container, text="WORLD", font=("Arial", 14, "bold"), fg="blue", bg="#aedef8")
            label.pack()
            self.user_input = tk.Entry(self.container, font=("Arial", 14))
            self.user_input.pack(pady=10)
            self.user_input.bind("<Key>", lambda e: label.config(text=""))

        elif q["type"] == "recall_words":
            self.user_input = tk.Entry(self.container, font=("Arial", 14))
            self.user_input.pack(pady=10)

        elif q["type"] == "radio" or q["type"] == "mcq" or q["type"] == "image_radio":
            self.var = tk.StringVar(value=" ")
            if q.get("image"):
                try:
                    img = PhotoImage(file=q["image"])
                    img = img.subsample(2, 2)
                    tk.Label(self.container, image=img, bg="#aedef8").pack()
                    self.container.image = img
                except:
                    tk.Label(self.container, text="[Image not available]", font=("Arial", 12), bg="#aedef8").pack()
            for opt in q["options"]:
                tk.Radiobutton(self.container, text=opt.title(), variable=self.var, value=opt.lower(), 
                               bg="#aedef8", font=("Arial", 14)).pack(anchor="w")

        elif q["type"] == "checkbox":
            self.vars = {}
            for opt in q["options"]:
                var = tk.IntVar()
                self.vars[opt] = var
                tk.Checkbutton(self.container, text=opt, variable=var, font=("Arial", 14), bg="#aedef8").pack(anchor="w")

        elif q["type"] == "serial7s":
            self.user_input = tk.Entry(self.container, font=("Arial", 14))
            self.user_input.pack(pady=10)

        elif q["type"] == "button":
            self.var = tk.StringVar()
            tk.Button(self.container, text="Done", command=lambda: self.var.set("done"), 
                      bg="#4CAF50", fg="white", font=("Arial", 14)).pack(pady=20)

        elif q["type"] == "info":
            pass

        next_btn = tk.Button(
            self.container,
            text="Next",
            command=self.evaluate_answer,
            font=("Arial", 14),
            bg="#2196F3",
            fg="white"
        )
        next_btn.place(relx=0.5, rely=1.0, anchor="s", y=-30)  # Bottom center with some margin


    def evaluate_sentence(self, text):
        return 1 if len(text.split()) >= 3 else 0

    def evaluate_answer(self):
        q = self.questions[self.current_question]
        result = 0
        given = ""

        if q["type"] in ["entry", "entry_disappear"]:
            given = self.user_input.get().strip().lower()
            if "custom_eval" in q:
                result = q["custom_eval"](given)
            elif given == q["answer"]:
                result = 1

        elif q["type"] == "recall_words":
            given = self.user_input.get().strip().lower().split()
            correct = q["answer"]
            result = sum([1 for word in given if word in correct])

        elif q["type"] in ["radio", "mcq", "image_radio"]:
            given = self.var.get().strip().lower()
            if given == q["answer"]:
                result = 1

        elif q["type"] == "serial7s":
            given = self.user_input.get().strip().split()
            correct = q["answer"]
            result = sum([1 for u, c in zip(given, correct) if u == c])

        elif q["type"] == "checkbox":
            selected = [k for k, v in self.vars.items() if v.get() == 1]
            result = 3 if set(selected) == set(q["answer"]) else 0
            given = ", ".join(selected)

        elif q["type"] == "button":
            given = self.var.get().strip().lower()
            if given == q["answer"]:
                result = 1

        self.responses.append((self.current_question + 1, q["question"], given, q.get("answer"), result))
        self.score += result
        self.current_question += 1
        self.show_question()

    def finish_test(self):
        result_window = tk.Toplevel(self)
        result_window.title("MMSE Test Results")
        result_window.geometry("600x500")

        # Frame to hold everything
        frame = tk.Frame(result_window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        summary = f"Your MMSE Score is: {self.score}/30\n\nScore Breakdown:\n"
        for q_no, question, user_ans, correct_ans, sc in self.responses:
            summary += f"Q{q_no}: {question[:30]}...\nYour Answer: {user_ans}\nExpected: {correct_ans}\nScore: {sc} {'\u2713' if sc else 'X'}\n\n"

        txt = scrolledtext.ScrolledText(frame, wrap=tk.WORD, font=("Arial", 12), height=15)
        txt.insert(tk.END, summary)
        txt.config(state="disabled")
        txt.pack(fill="both", expand=False)

        # Final score label
        tk.Label(frame, text=f"Final MMSE Score: {self.score}/30",
                font=("Arial", 16, "bold"), fg="green").pack(pady=10)

        # Submit button
        submit_button = tk.Button(self, text="Submit", command=self.on_submit)
        submit_button.pack(pady=10)

    def on_submit(self):
        # Save score to a temp file
        temp_file_path = os.path.join(tempfile.gettempdir(), "mmse_score.txt")
        with open(temp_file_path, "w") as f:
            f.write(str(self.score))

        messagebox.showinfo("Submitted", "MMSE score submitted successfully!")
        self.destroy()  # Close MMSE test window


if __name__ == "__main__":
    app = MMSETestApp()
    app.mainloop()
