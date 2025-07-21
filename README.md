# 🧠 Dementia Detection Using MMSE and Machine Learning

This project is a GUI-based system to assist in the early diagnosis of dementia. It integrates a user-friendly interface with a dynamic MMSE (Mini-Mental State Examination) test and a machine learning model (Random Forest) to predict the likelihood of dementia based on medical and cognitive inputs.

## 🌟 Features

- User authentication system (Login/Register)
- Dynamic MMSE test with one question per screen
- Automatic MMSE score calculation and integration
- Dementia prediction using trained Random Forest model
- User-friendly GUI built with Tkinter
- History tracking of predictions and login activity

## 🛠️ Tech Stack

- **Programming Language:** Python  
- **GUI:** Tkinter  
- **Machine Learning:** scikit-learn (Random Forest)  
- **Data Handling:** pandas, numpy  
- **Database:** MySQL  
- **Other Tools:** PIL (for images), datetime, file handling

## 📁 Folder Structure
dementia-detection/
│
├── mess.py # Main application file
├── mmse_test_gui.py # Dynamic MMSE test window logic
├── model.pkl # Trained ML model
├── database.sql # SQL script for database
├── assets/ # Icons and images
├── screenshots/ # UI screenshots
└── README.md # Project documentation


## 🚀 How to Run the Project

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/dementia-detection.git
   cd dementia-detection
2. Install libraries
   pip install pandas numpy scikit-learn pillow mysql-connector-python
3. Set up the MySQL database
  Start your MySQL server.
  Run the database.sql script to create required tables.
  Update the database credentials in the Python files (host, user, password, database).
4. Run the Application
  python mess.py


🤖 Machine Learning Model
Algorithm Used: Random Forest Classifier
Input Features: Age, BMI, Blood Pressure, MMSE Score
Accuracy: ~93% (based on training dataset)
Output: Predicts "Dementia Likely" or "Not Likely"

🧑‍💻 Author
Poojitha Polamarasetti
MCA Student | Frontend & Data Enthusiast

📜 License
This project is for academic and educational purposes only. Not intended for real medical use.
