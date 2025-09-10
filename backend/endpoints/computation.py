from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from database.database import save_string
from computation.parser import Parser
# Create router for compute endpoints
router = APIRouter(prefix="/compute", tags=["compute"])


# Request model for string input
class ComputationRequest(BaseModel):
    text: str


# Response model
class ComputationResponse(BaseModel):
    output: int

# Compute endpoint
@router.post("", response_model=ComputationResponse)
async def parse_string(request: ComputationRequest):
    """Compute endpoint that saves the input string to database and returns result of computation"""
    parser = Parser()
    try:
        result = parser.parse_expression(request.text)
        string_id = save_string(request.text)
        # Для целочисленного деления показываем целые числа без .0 где возможно
        if result.is_integer():
            return ComputationResponse(int(result))
        else:
            return ComputationResponse(result)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e
        )