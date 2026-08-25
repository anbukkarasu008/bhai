from groq import Groq

from backend.app.config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

client = Groq(
    api_key=GROQ_API_KEY
)


def rewrite_question(question: str, history: list):
    """
    Rewrite the user's latest question into a standalone question
    using the previous conversation.

    The rewriter must resolve references such as:
    it, its, they, this, that, etc.

    It must never introduce an entity that is not present
    in the conversation history or current question.
    """

    try:

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a question rewriting component in a "
                    "Conversational RAG system.\n\n"

                    "Your ONLY task is to rewrite the user's latest "
                    "question into a standalone question.\n\n"

                    "STRICT RULES:\n"

                    "1. Use ONLY information explicitly present in "
                    "the conversation history or the latest question.\n"

                    "2. NEVER invent, assume, or introduce a new "
                    "person, company, product, organization, object, "
                    "or entity.\n"

                    "3. When the latest question contains a reference "
                    "such as 'it', 'its', 'they', 'them', 'this', "
                    "'that', or 'the product', resolve the reference "
                    "using the most recent relevant entity from the "
                    "conversation.\n"

                    "4. Preserve the exact entity name from the "
                    "conversation. Do NOT replace it with another "
                    "entity.\n"

                    "5. Preserve the original meaning of the question.\n"

                    "6. Do NOT answer the question.\n"

                    "7. Do NOT add explanations.\n"

                    "8. Return ONLY the rewritten standalone question.\n\n"

                    "Example:\n"
                    "Conversation:\n"
                    "User: What is InferAPI?\n"
                    "Assistant: InferAPI is an API documentation system.\n"
                    "User: What problem does it solve?\n\n"
                    "Correct rewrite:\n"
                    "What problem does InferAPI solve?\n\n"

                    "Incorrect rewrite:\n"
                    "What problem does OpenAI's ChatGPT solve?\n\n"

                    "If the reference cannot be resolved confidently, "
                    "return the user's original question unchanged."
                )
            }
        ]

        # Add previous conversation
        messages.extend(history)

        # Add the latest user question
        messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0
        )

        rewritten_question = (
            response.choices[0]
            .message.content
            .strip()
        )

        return rewritten_question

    except Exception as e:

        print("Query Rewrite Error:", e)

        # If rewriting fails, use the original question
        return question