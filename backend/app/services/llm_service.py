from groq import Groq

from backend.app.config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

from backend.app.services.memory_service import get_history


# --------------------------------------------------
# Groq client
# --------------------------------------------------

client = Groq(
    api_key=GROQ_API_KEY
)


def generate_response(
    question: str,
    context: str,
    session_id: str
):
    """
    Generate an answer using the retrieved document context
    and the conversation history for the current session.
    """

    # --------------------------------------------------
    # Step 1: Check whether retrieval returned context
    # --------------------------------------------------

    if not context.strip():
        return "I don't know based on the provided document."

    try:

        # --------------------------------------------------
        # Step 2: System instructions
        # --------------------------------------------------

        messages = [
    {
        "role": "system",
        "content": (
            "You are a document question-answering assistant.\n\n"

            "Your job is to answer the CURRENT QUESTION using "
            "ONLY the CURRENT RETRIEVED CONTEXT.\n\n"

            "IMPORTANT RULES:\n"
            "1. The CURRENT RETRIEVED CONTEXT is the only source "
            "of factual information.\n"

            "2. Do NOT use your own knowledge or outside information.\n"

            "3. Do NOT use previous assistant answers as factual "
            "evidence.\n"

            "4. Conversation history may ONLY help resolve "
            "references such as 'it', 'they', 'this', or 'that'.\n"

            "5. If the CURRENT RETRIEVED CONTEXT contains enough "
            "information to answer the CURRENT QUESTION, answer "
            "using that information.\n"

            "6. If the CURRENT RETRIEVED CONTEXT does not contain "
            "enough information, respond exactly with:\n"
            "I don't know based on the provided document.\n"

            "7. Do not guess, assume, or invent information.\n"

            "8. Keep the answer clear and directly related to the "
            "CURRENT QUESTION."
        ),
    }
]

        # --------------------------------------------------
        # Step 3: Get conversation history
        # --------------------------------------------------

        history = get_history(session_id)

        # --------------------------------------------------
        # Step 4: Add conversation history
        # --------------------------------------------------

        messages.extend(history)

        # --------------------------------------------------
        # Step 5: Add current question + retrieved context
        # --------------------------------------------------
        messages.append(
    {
        "role": "user",
        "content": f"""
        ==============================
        CURRENT RETRIEVED DOCUMENT
        ==============================

        {context}

        ==============================
        CURRENT QUESTION
        ==============================

        {question}

        ==============================
        ANSWERING INSTRUCTION
        ==============================
        Answer the CURRENT QUESTION using only the CURRENT RETRIEVED DOCUMENT.
        """
    }
)
         
        # Step 6: Generate response
        # --------------------------------------------------

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages
        )

        # --------------------------------------------------
        # Step 7: Return answer
        # --------------------------------------------------

        return response.choices[0].message.content.strip()

    except Exception as e:

        print("Groq Error:", e)

        return "Unable to generate an answer at this time."