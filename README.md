# Loan Approval Prediction Pro

Full-stack ML project using FastAPI, Scikit-learn, SQLite and HTML/CSS/JavaScript.

## Features
- Premium responsive dashboard
- Login and registration
- SQLite user database
- Loan prediction API
- Random Forest model
- Confidence score
- Prediction history
- Dashboard statistics
- FastAPI Swagger docs

## Run on Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r backend\requirements.txt
uvicorn backend.main:app --reload
```
Then open `frontend/index.html`.

API docs: http://127.0.0.1:8000/docs

The included dataset is synthetic and for educational/demo use only.

## V2 Analytics
- Model comparison: Logistic Regression, Decision Tree, Random Forest
- Accuracy, Precision, Recall and F1 Score
- Best-model selection by F1 score
- Confusion matrix
- Dataset summary
- New `/analytics` endpoint
- Analytics dashboard section
