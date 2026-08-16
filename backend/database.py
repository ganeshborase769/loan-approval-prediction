import sqlite3
from pathlib import Path
from contextlib import contextmanager
DB_PATH=Path(__file__).parent/"loan_app.db"
@contextmanager
def get_db():
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row
    try: yield c; c.commit()
    finally: c.close()
def init_db():
    with get_db() as d:
        d.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,email TEXT UNIQUE,password TEXT,created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        d.execute("CREATE TABLE IF NOT EXISTS predictions(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER,applicant_income REAL,coapplicant_income REAL,loan_amount REAL,credit_history INTEGER,property_area TEXT,prediction TEXT,probability REAL,created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
