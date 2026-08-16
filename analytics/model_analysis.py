from pathlib import Path
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

BASE=Path(__file__).resolve().parent.parent
df=pd.read_csv(BASE/"dataset"/"loan_data.csv")
X=df.drop(columns="Loan_Status"); y=(df["Loan_Status"]=="Y").astype(int)

cat=["Gender","Married","Dependents","Education","Self_Employed","Property_Area"]
num=["ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History"]
pre=ColumnTransformer([
 ("num",Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler())]),num),
 ("cat",Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("onehot",OneHotEncoder(handle_unknown="ignore"))]),cat)
])
models={
 "Logistic Regression":LogisticRegression(max_iter=1000),
 "Decision Tree":DecisionTreeClassifier(max_depth=6,random_state=42),
 "Random Forest":RandomForestClassifier(n_estimators=250,random_state=42,class_weight="balanced")
}
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
results=[]
for name,clf in models.items():
    pipe=Pipeline([("preprocessor",pre),("classifier",clf)])
    pipe.fit(Xtr,ytr); pred=pipe.predict(Xte)
    results.append({
        "Model":name,
        "Accuracy":round(accuracy_score(yte,pred)*100,2),
        "Precision":round(precision_score(yte,pred,zero_division=0)*100,2),
        "Recall":round(recall_score(yte,pred,zero_division=0)*100,2),
        "F1 Score":round(f1_score(yte,pred,zero_division=0)*100,2)
    })
best=max(results,key=lambda x:x["F1 Score"])
print(pd.DataFrame(results).to_string(index=False))
print("\nBest model:",best["Model"])
