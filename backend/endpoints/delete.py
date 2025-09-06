from fastapi import HTTPException
from pydantic import BaseModel
from database.database import delete_all_strings, DatabaseError, DatabaseQueryError

# Response model
class DeleteResponse(BaseModel):
    message: str
    deleted_count: int

def delete_all_content() -> DeleteResponse:
    """Delete all content from the database"""
    try:
        deleted_count = delete_all_strings()
        return DeleteResponse(
            message=f"Successfully deleted {deleted_count} records from the database",
            deleted_count=deleted_count
        )
    except DatabaseQueryError as e:
        raise HTTPException(status_code=500, detail="Failed to delete strings from database")
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
