# 🏦 Loan Approval Prediction System

A full-stack Machine Learning web application that predicts whether a loan application is likely to be approved based on applicant information.

The project combines Machine Learning, FastAPI, SQLite and a responsive HTML/CSS/JavaScript dashboard.

---

## 🚀 Features

- 🔐 User Registration & Login
- 🧠 Machine Learning based loan prediction
- 🎯 Prediction confidence score
- 📊 Dashboard with application statistics
- 📋 Prediction history
- 🤖 Multiple ML model comparison
- 📈 Accuracy, Precision, Recall and F1 Score
- 📉 Confusion Matrix
- 🏆 Best model identification
- 🗄️ SQLite database
- ⚡ FastAPI REST API
- 📱 Responsive frontend
- 📚 FastAPI Swagger API documentation

---

## 🧠 Machine Learning

The project evaluates multiple Machine Learning algorithms:

| Model | Evaluation |
|---|---|
| Logistic Regression | Accuracy, Precision, Recall, F1 |
| Decision Tree | Accuracy, Precision, Recall, F1 |
| Random Forest | Accuracy, Precision, Recall, F1 |

The best-performing model is selected based on the F1 Score.

### Input Features

- Gender
- Married
- Dependents
- Education
- Self Employed
- Applicant Income
- Coapplicant Income
- Loan Amount
- Loan Term
- Credit History
- Property Area

---

## 📊 Model Evaluation

The application provides:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

The analytics dashboard allows comparison between different Machine Learning models.

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- FastAPI
- Pydantic
- SQLite

### Machine Learning
- Scikit-learn
- Pandas
- NumPy
- Joblib

### Development Tools
- VS Code
- Git
- GitHub

---

## 📁 Project Structure

```text
Loan-Approval-Prediction-Pro-v2/
│
├── analytics/
│   └── model_analysis.py
│
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── requirements.txt
│
├── dataset/
│   └── loan_data.csv
│
├── docs/
│   └── project_features.md
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── .gitignore
│
├── model/
│   └── loan_model.pkl
│
├── .gitignore
└── README.md

## ⚙️ Installation & Setup


### 1. Clone the repository


```bash
git clone https://github.com/ganeshborase769/loan-approval-prediction.git
2. Open the project
cd loan-approval-prediction
3. Create virtual environment
python -m venv venv
4. Activate virtual environment

Windows:

venv\Scripts\activate
5. Install dependencies
pip install -r backend/requirements.txt
6. Start the FastAPI server
uvicorn backend.main:app --reload

Backend will run at:

http://127.0.0.1:8000
7. API Documentation

Open:

http://127.0.0.1:8000/docs
8. Start the Frontend

Open:

frontend/index.html

in your browser.

🔄 How It Works
User
  ↓
Register / Login
  ↓
Enter Loan Details
  ↓
FastAPI Backend
  ↓
Machine Learning Model
  ↓
Loan Prediction
  ↓
Approval / Not Approved
  ↓
Confidence Score
  ↓
SQLite Database
  ↓
Prediction History
📊 Model Analytics

The project includes a Machine Learning Analytics dashboard.

It compares:

Logistic Regression
Decision Tree
Random Forest

Evaluation metrics include:

Accuracy
Precision
Recall
F1 Score
Confusion Matrix

The best model is selected based on F1 Score.

🎯 Key Highlights
Full-stack Machine Learning application
REST API using FastAPI
User authentication
Real-time loan prediction
Model confidence score
Prediction history
SQLite database integration
Machine Learning model comparison
Responsive dashboard
Interactive API documentation
🚀 Future Improvements
Deploy the application on cloud
Add Admin Dashboard
Add interactive charts
Add downloadable prediction reports
Train models using a larger real-world dataset
Add more Machine Learning algorithms
👨‍💻 Author
Ganesh Borse

MCA Student | Aspiring Frontend Developer | Machine Learning Enthusiast

Technologies:
Python • Machine Learning • FastAPI • SQLite • HTML • CSS • JavaScript • Scikit-learn

📌 Disclaimer

This project is developed for educational and demonstration purposes. Loan predictions should not be used as the sole basis for real financial decisions.