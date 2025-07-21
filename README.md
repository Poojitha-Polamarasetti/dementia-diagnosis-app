<img width="872" height="906" alt="test score" src="https://github.com/user-attachments/assets/98e0b0ed-e170-493f-a97d-ddcf8333ce56" />
<img width="1920" height="1014" alt="registration screen" src="https://github.com/user-attachments/assets/ed0f37f6-0d18-4e7e-aeca-b020b99bf5a2" />
<img width="874" height="910" alt="mmse test" src="https://github.com/user-attachments/assets/14655839-e404-41fe-b8e9-131ab9873b10" />
<img width="1657" height="1021" alt="menu screen" src="https://github.com/user-attachments/assets/9153add5-9f78-43eb-af68-e67efe1661a3" />
<img width="1920" height="1020" alt="medical test" src="https://github.com/user-attachments/assets/d2007362-073b-4d52-9b5f-bece3375c398" />
<img width="1920" height="1020" alt="login screen" src="https://github.com/user-attachments/assets/eb6d5761-5e56-453e-bc47-e3d27c02fd6b" />
<img width="1920" height="1022" alt="history screen" src="https://github.com/user-attachments/assets/1f4ad2d5-a51a-4ea2-89eb-1da3fff57ee7" />
<img width="604" height="513" alt="forgot password" src="https://github.com/user-attachments/assets/f24a662a-3523-46e3-bd3b-010d013da589" />
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
Input Features: Age, BMI, lifestyle, MMSE Score
Accuracy: ~93% (based on training dataset)
Output: Predicts "Dementia Likely" or "Not Likely"

🧑‍💻 Author
Poojitha Polamarasetti
MCA Student | Frontend & Data Enthusiast

📜 License
This project is for academic and educational purposes only. Not intended for real medical use.
