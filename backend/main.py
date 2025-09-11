from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from typing import Union

from database.database import (
    init_database, DatabaseInitializationError,
    save_calculation, get_all_calculations, delete_all_calculations,
)
from computation.parser import Parser 

try:
    init_database()
except DatabaseInitializationError as e:
    print(f"Failed to initialize database: {e}")
    raise

app = FastAPI(title="Calculator API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=False,    
    allow_methods=["*"],
    allow_headers=["*"],
)

class CalcRequest(BaseModel):
    expression: str

class CalcResponse(BaseModel):
    result: Union[float, int, str]

SAFE_INT_LIMIT = 2**53

def to_response_number(val):
    if isinstance(val, float) and val.is_integer() and abs(val) <= SAFE_INT_LIMIT:
        return int(val)
    return val

def pretty_number(val) -> str:
    if isinstance(val, (int,)):
        return str(val)
    if isinstance(val, float):
        return f"{val:.15g}"
    return str(val)

def pretty_expression(expr: str) -> str:
    return (expr.replace('**', '^')
                .replace('*', '×')
                .replace('/', '÷')
                .replace('.', ','))

@app.post("/calculate", response_model=CalcResponse)
def calculate(req: CalcRequest):
    parser = Parser()
    try:
        val = parser.parse_expression(req.expression)
        out = to_response_number(val)
        expr_for_history = pretty_expression(req.expression)
        result_for_history = pretty_number(val) 
        save_calculation(expr_for_history, result_for_history)
        return {"result": out}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@app.get("/history")
def history():
    return get_all_calculations()

@app.delete("/delete/all")
def delete_all():
    return {"deleted": delete_all_calculations()}

@app.get("/health")
def health():
    return {"ok": True}

