from fastapi import APIRouter
from pydantic import BaseModel
from database.database import delete_all_strings

# Create router for delete endpoints
router = APIRouter(prefix="/delete", tags=["delete"])

# Response model
class DeleteResponse(BaseModel):
    message: str
    deleted_count: int

# Delete all content endpoint
@router.delete("/all", response_model=DeleteResponse)
async def delete_all_content():
    """Delete all content from the database"""
    deleted_count = delete_all_strings()
    
    return {
        "message": f"Successfully deleted {deleted_count} records from the database",
        "deleted_count": deleted_count
    }