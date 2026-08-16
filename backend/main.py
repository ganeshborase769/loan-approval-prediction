from pathlib import Path
import hashlib,secrets,sqlite3,joblib,pandas as pd
from typing import Optional
from fastapi import FastAPI,HTTPException,Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
from .database import init_db,get_db
BASE = Path(__file__).resolve().parent.parent
app=FastAPI(title="Loan Approval Prediction Pro")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
init_db(); model=joblib.load(Path(__file__).parent.parent/"model"/"loan_model.pkl"); tokens={}
class Register(BaseModel):
    name:str=Field(min_length=2); email:str; password:str=Field(min_length=6)
class Login(BaseModel): email:str; password:str
class Loan(BaseModel):
    Gender:str; Married:str; Dependents:str; Education:str; Self_Employed:str
    ApplicantIncome:float=Field(gt=0); CoapplicantIncome:float=Field(ge=0); LoanAmount:float=Field(gt=0)
    Loan_Amount_Term:int=Field(gt=0); Credit_History:int=Field(ge=0,le=1); Property_Area:str
def ph(p): return hashlib.sha256(p.encode()).hexdigest()
def uid(a:Optional[str]):
    if not a or not a.startswith("Bearer ") or a[7:] not in tokens: raise HTTPException(401,"Login required")
    return tokens[a[7:]]

@app.get("/analytics")
def analytics():
    """Model/dataset analytics for the dashboard."""
    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.impute import SimpleImputer
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
    from sklearn.linear_model import LogisticRegression
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier
    df=pd.read_csv(BASE/"dataset"/"loan_data.csv")
    X=df.drop(columns="Loan_Status"); y=(df["Loan_Status"]=="Y").astype(int)
    cats=["Gender","Married","Dependents","Education","Self_Employed","Property_Area"]
    nums=["ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History"]
    pre=ColumnTransformer([("num",Pipeline([("imp",SimpleImputer(strategy="median")),("scale",StandardScaler())]),nums),
                           ("cat",Pipeline([("imp",SimpleImputer(strategy="most_frequent")),("oh",OneHotEncoder(handle_unknown="ignore"))]),cats)])
    models={"Logistic Regression":LogisticRegression(max_iter=1000),
            "Decision Tree":DecisionTreeClassifier(max_depth=6,random_state=42),
            "Random Forest":RandomForestClassifier(n_estimators=250,random_state=42,class_weight="balanced")}
    Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
    metrics=[]; cms={}
    for name,clf in models.items():
        pipe=Pipeline([("preprocessor",pre),("classifier",clf)])
        pipe.fit(Xtr,ytr); pred=pipe.predict(Xte)
        metrics.append({"model":name,"accuracy":round(accuracy_score(yte,pred)*100,2),
                        "precision":round(precision_score(yte,pred,zero_division=0)*100,2),
                        "recall":round(recall_score(yte,pred,zero_division=0)*100,2),
                        "f1":round(f1_score(yte,pred,zero_division=0)*100,2)})
        cms[name]=confusion_matrix(yte,pred).tolist()
    best=max(metrics,key=lambda x:x["f1"])
    return {"dataset":{"rows":len(df),"approved":int((df.Loan_Status=="Y").sum()),
                       "rejected":int((df.Loan_Status=="N").sum())},
            "metrics":metrics,"best_model":best["model"],"confusion_matrices":cms}

@app.get("/")
def root(): return {"status":"ok"}
@app.post("/auth/register")
def register(x:Register):
    with get_db() as d:
        try: cur=d.execute("INSERT INTO users(name,email,password) VALUES(?,?,?)",(x.name,x.email.lower(),ph(x.password))); u=cur.lastrowid
        except sqlite3.IntegrityError: raise HTTPException(409,"Email already registered")
    t=secrets.token_urlsafe(32); tokens[t]=u; return {"token":t,"user":{"id":u,"name":x.name,"email":x.email.lower()}}
@app.post("/auth/login")
def login(x:Login):
    with get_db() as d: r=d.execute("SELECT * FROM users WHERE email=?",(x.email.lower(),)).fetchone()
    if not r or r["password"]!=ph(x.password): raise HTTPException(401,"Invalid email or password")
    t=secrets.token_urlsafe(32); tokens[t]=r["id"]; return {"token":t,"user":{"id":r["id"],"name":r["name"],"email":r["email"]}}
@app.get("/auth/me")
def me(authorization:Optional[str]=Header(None)):
    with get_db() as d: r=d.execute("SELECT id,name,email FROM users WHERE id=?",(uid(authorization),)).fetchone()
    return dict(r)
@app.post("/predict")
def predict(x:Loan,authorization:Optional[str]=Header(None)):
    u=uid(authorization); row=pd.DataFrame([x.model_dump()]); p=int(model.predict(row)[0]); conf=round(float(model.predict_proba(row)[0][p])*100,2); result="Approved" if p else "Not Approved"
    with get_db() as d: d.execute("INSERT INTO predictions(user_id,applicant_income,coapplicant_income,loan_amount,credit_history,property_area,prediction,probability) VALUES(?,?,?,?,?,?,?,?)",(u,x.ApplicantIncome,x.CoapplicantIncome,x.LoanAmount,x.Credit_History,x.Property_Area,result,conf))
    return {"prediction":result,"probability":conf}
@app.get("/predictions")
def history(authorization:Optional[str]=Header(None)):
    with get_db() as d: r=d.execute("SELECT * FROM predictions WHERE user_id=? ORDER BY id DESC",(uid(authorization),)).fetchall()
    return [dict(x) for x in r]
@app.get("/stats")
def stats(authorization:Optional[str]=Header(None)):
    u=uid(authorization)
    with get_db() as d:
        t=d.execute("SELECT COUNT(*) c FROM predictions WHERE user_id=?",(u,)).fetchone()["c"]; a=d.execute("SELECT COUNT(*) c FROM predictions WHERE user_id=? AND prediction='Approved'",(u,)).fetchone()["c"]
    return {"total":t,"approved":a,"rejected":t-a,"approval_rate":round(a/t*100,1) if t else 0}
