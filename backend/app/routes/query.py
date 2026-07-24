from fastapi import APIRouter
from backend.app.schemas.query_schema import QueryRequest
from backend.app.services.embedding_service import (
    generate_query_embedding,
    load_faiss_index
)
from backend.app.services.retrieval_service import (
    search_index,
    load_chunks
)

router = APIRouter()


@router.post("/query")
async def ask_question(request: QueryRequest):

    query_embedding = generate_query_embedding(request.question)

    index = load_faiss_index("backend/vector_store/faiss_index.bin")

    distances, indices = search_index(index, query_embedding)

    chunks = load_chunks("backend/vector_store/chunks.json")

    retrieved_chunks = []

    for idx in indices[0]:
        retrieved_chunks.append(chunks[idx])

    return {
    "question": request.question,
    "context": retrieved_chunks
}