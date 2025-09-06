from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sqlite3
import datetime
import ast
import operator as op
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), "storage", "calculations.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

conn = get_conn()
conn.execute("""
CREATE TABLE IF NOT EXISTS calculations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  expression TEXT NOT NULL,
  result TEXT NOT NULL,
  created_at TEXT NOT NULL
)""")
conn.commit()

app = FastAPI(title="Calculator API (stub)", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:3000", "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalcRequest(BaseModel):
    expression: str

ALLOWED_BIN = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
    ast.Div: op.truediv, ast.Pow: op.pow
}
ALLOWED_UN = {ast.UAdd: lambda x: +x, ast.USub: lambda x: -x}

_STORE: List[Dict[str, Any]] = []
_NEXT_ID = 1

def safe_eval(expr: str) -> float:
    raise NotImplementedError("Calculation is not implemented yet")

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/calculate")
def calculate(payload: CalcRequest):
    global _NEXT_ID, _STORE
    expr = (payload.expression or "").strip()
    created_at = datetime.datetime.utcnow().isoformat()

    row = {
        "id": _NEXT_ID,
        "expression": expr,
        "result": expr,
        "created_at": created_at,
    }
    _STORE.insert(0, row) 
    _NEXT_ID += 1
    return row

@app.get("/history")
def history():
    return _STORE

@app.delete("/delete/all")
def delete_all():
    deleted = len(_STORE)
    _STORE.clear()
    return {"deleted": deleted}
