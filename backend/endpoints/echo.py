from typing import List
from fastapi import HTTPException
from pydantic import BaseModel
from database.database import save_string, get_all_strings, DatabaseError, DatabaseQueryError

class StringRequest(BaseModel):
    text: str

class StringResponse(BaseModel):
    output: str
    id: int

class HistoryItem(BaseModel):
    id: int
    text: str
    created_at: str

async def echo_string(request: StringRequest):
    """Echo endpoint that saves the input string to database and returns it with ID"""
    try:
        string_id = save_string(request.text)
        return {"output": request.text, "id": string_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DatabaseQueryError as e:
        raise HTTPException(status_code=500, detail="Failed to save string to database")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

async def list_strings():
    """List all saved strings (newest first)"""
    try:
        return get_all_strings()
    except DatabaseQueryError as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve strings from database")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
