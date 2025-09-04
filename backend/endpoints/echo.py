from fastapi import APIRouter
from pydantic import BaseModel
from database.database import save_string

# Create router for echo endpoints
router = APIRouter(prefix="/echo", tags=["echo"])

# Request model for string input
class StringRequest(BaseModel):
    text: str

# Response model
class StringResponse(BaseModel):
    output: str
    id: int

# String output endpoint
@router.post("", response_model=StringResponse)
async def echo_string(request: StringRequest):
    """Echo endpoint that saves the input string to database and returns it with ID"""
    # Save string to database
    string_id = save_string(request.text)
    
    return {
        "output": request.text,
        "id": string_id
    }