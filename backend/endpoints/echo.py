from typing import List
from fastapi import APIRouter
from pydantic import BaseModel
from database.database import save_string, get_all_strings

router = APIRouter(prefix="/echo", tags=["echo"])

class StringRequest(BaseModel):
    text: str

class StringResponse(BaseModel):
    output: str
    id: int

class HistoryItem(BaseModel):
    id: int
    text: str
    created_at: str

@router.post("", response_model=StringResponse)
async def echo_string(request: StringRequest):
    """Echo endpoint that saves the input string to database and returns it with ID"""
    string_id = save_string(request.text)
    return {"output": request.text, "id": string_id}

@router.get("", response_model=List[HistoryItem])
async def list_strings():
    """List all saved strings (newest first)"""
    return get_all_strings()
