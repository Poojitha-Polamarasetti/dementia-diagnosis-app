'''#rfa
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("alzheimer_dataset.csv")

# Display first few rows
print(df.head())

# Assuming last column is the target (adjust as needed)
X = df.iloc[:, :-1]  
y = df.iloc[:, -1]   

# Convert categorical features (if any)
X = pd.get_dummies(X, drop_first=True)  

# Split dataset into training/testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")'''
'''
#svm model
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report

# Load dataset
df = pd.read_csv("alzheimer_dataset.csv")

# Strip spaces from column names to prevent hidden issues
df.columns = df.columns.str.strip()

# Verify column names
print("Columns:", df.columns)

# Drop ID column (not useful for prediction)
if "ID" in df.columns:
    df = df.drop(columns=["ID"])

# Check if Diagnosis column exists before dropping
if "Diagnosis" in df.columns:
    X = df.drop(columns=["Diagnosis"])
    y = df["Diagnosis"]
else:
    raise KeyError("Column 'Diagnosis' not found. Check dataset.")

# Encode categorical variables
X = pd.get_dummies(X, drop_first=True)

# Standardize features for SVM
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split dataset into training/testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train SVM model
svm_model = SVC(kernel="linear")
svm_model.fit(X_train, y_train)

# Make predictions
y_pred = svm_model.predict(X_test)

# Evaluate model performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))'''

#Random forest algorithm main

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Load dataset
df = pd.read_csv("alzheimer_dataset.csv")
df.columns = df.columns.str.strip()

# Drop ID if present
if "ID" in df.columns:
    df = df.drop(columns=["ID"])

# Target and Features
X = df.drop(columns=["Diagnosis"])
y = df["Diagnosis"]

# Manual encoding (replace categories with numbers)
# Use the actual column name as per your CSV
X["Gender"] = X["Gender"].map({"Male": 1, "Female": 0})
X["Smoking"] = X["Smoking"].map({"Yes": 1, "No": 0})
X["Alcohol Consumption"] = X["Alcohol Consumption"].map({"Yes": 1, "No": 0})
X["Physical Activity"] = X["Physical Activity"].map({"Low": 0, "Moderate": 1, "High": 2})
print("Min age:", df["Age"].min())
print("Max age:", df["Age"].max())
# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save model & features
joblib.dump(model, "dementia_model.pkl")
joblib.dump(X.columns.tolist(), "model_features.pkl")

