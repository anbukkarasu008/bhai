from fastapi import APIRouter, HTTPException
from backend.app.schemas.query_schema import QueryRequest
from backend.app.services.retrieval_service import retrieve_context
from backend.app.services.llm_service import generate_response
from backend.app.services.memory_service import (
    add_message,
    get_history,
    clear_history
)
from backend.app.services.query_rewrite_service import rewrite_question

router = APIRouter()


@router.post("/query")
async def ask_question(request: QueryRequest):

    try:

        # --------------------------------------------------
        # Step 1: Get previous conversation
        # --------------------------------------------------

        history = get_history(
            request.session_id
        )

        # --------------------------------------------------
        # Step 2: Rewrite the question
        # --------------------------------------------------

        rewritten_question = rewrite_question(
            question=request.question,
            history=history
        )

        # --------------------------------------------------
        # Step 3: Retrieve relevant context
        # --------------------------------------------------

        retrieval_result = retrieve_context(
            rewritten_question
        )

        context = retrieval_result["context"]

        sources = retrieval_result["sources"]

        # --------------------------------------------------
        # Step 4: Generate answer
        # --------------------------------------------------

        answer = generate_response(
            question=rewritten_question,
            context=context,
            session_id=request.session_id
        )

        # --------------------------------------------------
        # Step 5: Save user question
        # --------------------------------------------------

        add_message(
            session_id=request.session_id,
            role="user",
            content=request.question
        )

        # --------------------------------------------------
        # Step 6: Save assistant answer
        # --------------------------------------------------

        add_message(
            session_id=request.session_id,
            role="assistant",
            content=answer
        )

        # --------------------------------------------------
        # Step 7: Return response
        # --------------------------------------------------

        return {
            "session_id": request.session_id,
            "question": request.question,
            "answer": answer,
            "rewritten_question": rewritten_question,
            "context": context,
            "sources": sources
        }

    except RuntimeError as e:

        print("Query processing error:", e)

        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve information from the document store."
        )


@router.get("/history/{session_id}")
async def get_conversation_history(session_id: str):

    return {
        "session_id": session_id,
        "history": get_history(session_id)
    }


@router.delete("/history/{session_id}")
async def clear_conversation_history(session_id: str):

    clear_history(session_id)

    return {
        "session_id": session_id,
        "message": "Conversation history cleared successfully"
    }