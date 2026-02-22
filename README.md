# 🧠 Dementia Detection Using MMSE and Machine Learning

A GUI-based application designed to assist in early dementia risk assessment by integrating a dynamic MMSE test with a trained Random Forest classification model.

---

## 📌 Project Overview

This system combines cognitive assessment scoring (MMSE) with a machine learning model to predict the likelihood of dementia based on medical and behavioral inputs.

The application provides:

- User authentication (Login/Register)
- Dynamic MMSE test (one question per screen)
- Automatic MMSE score calculation
- Random Forest-based dementia prediction
- MySQL-backed data storage
- Prediction history tracking

This project was developed as a final-year MCA application integrating machine learning, GUI development, and database management.

---

## 🤖 Machine Learning Model

- **Algorithm Used:** Random Forest Classifier  
- **Input Features:** Age, BMI, Blood Pressure, MMSE Score  
- **Accuracy:** ~93% (evaluated on test dataset)  
- **Output:** “Dementia Likely” / “Not Likely”

---

## 🛠 Tech Stack

- **Programming Language:** Python  
- **GUI Framework:** Tkinter  
- **Machine Learning:** scikit-learn  
- **Data Handling:** pandas, numpy  
- **Database:** MySQL  
- **Other Libraries:** Pillow, datetime  

---

## 🗂 Project Structure
dementia-diagnosis-app/
│
├── app/
│   ├── main_app.py
│   ├── mmse_test_gui.py
│
├── model/
│   ├── dementia_model.pkl
│   ├── model_features.pkl
│
├── data/
│   ├── alzheimer_dataset.csv
│
├── training/
│   ├── model_training.py
│
├── reports/
│   ├── dementia_report.pdf
│
└── README.md

---

## 🚀 How to Run

### 1️⃣ Clone Repository
git clone https://github.com/Poojitha-Polamarasetti/dementia-diagnosis-app.git

cd dementia-diagnosis-app

### 2️⃣ Install Dependencies
pip install pandas numpy scikit-learn pillow mysql-connector-python


### 3️⃣ Configure Database
- Start MySQL server
- Execute `database.sql`
- Update database credentials in Python files

### 4️⃣ Run Application
python main.py


---

## ⚠ Disclaimer

This system is developed for academic and demonstration purposes only.  
It is not intended for real-world medical diagnosis.

---

## 👩‍💻 Author

Poojitha Polamarasetti  
MCA Graduate | Python & Machine Learning
