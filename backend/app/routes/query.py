from fastapi import APIRouter
from backend.app.schemas.query_schema import QueryRequest

router = APIRouter()


@router.post("/query")
async def ask_question(request: QueryRequest):
    return {
        "question": request.question,
        "message": "Query received successfully."
    }