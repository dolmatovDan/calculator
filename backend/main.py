from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

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
    allow_origins=[
        "http://localhost:5173","http://127.0.0.1:5173",
        "http://localhost:3000","http://127.0.0.1:3000",
    ],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

class CalcRequest(BaseModel):
    expression: str

class CalcResponse(BaseModel):
    result: float | int | str

@app.post("/calculate")
def calculate(req: CalcRequest):
    parser = Parser()
    try:
        val = parser.parse_expression(req.expression)
        out = int(val) if isinstance(val, float) and val.is_integer() else val
        save_calculation(req.expression, str(out))
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

