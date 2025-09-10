from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import sqlite3
import datetime
import ast
import operator as op
from typing import List, Dict, Any

from database.database import init_database, DatabaseInitializationError
from endpoints.delete import delete_all_content
from computation.parser import Parser

DB_PATH = os.path.join(os.path.dirname(__file__), "storage", "calculations.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize database with error handling
try:
    init_database()
except DatabaseInitializationError as e:
    print(f"Failed to initialize database: {e}")
    exit(1)

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

@app.post("/save")
def safe_eval(expr: str) -> float:
    """Compute endpoint that saves the input string to database and returns result of computation"""
    parser = Parser()
    try:
        result = parser.parse_expression(expr)
        # string_id = save_string(expr)
        # Для целочисленного деления показываем целые числа без .0 где возможно
        if result.is_integer():
            return int(result)
        else:
            return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )

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
    response = delete_all_content()
    
    return {"deleted": response.deleted_count}