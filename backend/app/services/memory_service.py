conversation_histories = {}

MAX_HISTORY_MESSAGES = 10


def add_message(session_id: str, role: str, content: str):

    if session_id not in conversation_histories:
        conversation_histories[session_id] = []

    conversation_histories[session_id].append(
        {
            "role": role,
            "content": content
        }
    )

    # Keep only the most recent messages
    conversation_histories[session_id] = (
        conversation_histories[session_id][-MAX_HISTORY_MESSAGES:]
    )


def get_history(session_id: str):

    if session_id not in conversation_histories:
        return []

    return conversation_histories[session_id]


def clear_history(session_id: str):

    if session_id in conversation_histories:
        conversation_histories[session_id].clear()