import re


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 100
):
    """
    Split text into sentence-aware chunks.

    The function tries to:
    - preserve complete sentences
    - keep chunks around chunk_size characters
    - provide sentence-level overlap
    """

    if not text or not text.strip():
        return []

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Split into sentences
    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    chunks = []
    current_sentences = []
    current_length = 0

    for sentence in sentences:

        sentence_length = len(sentence)

        # Add sentence if it fits
        if (
            current_sentences
            and current_length + sentence_length + 1 > chunk_size
        ):
            chunks.append(" ".join(current_sentences))

            # Create overlap using complete sentences
            overlap_sentences = []
            overlap_length = 0

            for previous_sentence in reversed(current_sentences):

                if overlap_length + len(previous_sentence) + 1 <= overlap:
                    overlap_sentences.insert(
                        0,
                        previous_sentence
                    )
                    overlap_length += (
                        len(previous_sentence) + 1
                    )
                else:
                    break

            current_sentences = overlap_sentences
            current_length = overlap_length

        current_sentences.append(sentence)
        current_length += sentence_length + 1

    # Add final chunk
    if current_sentences:
        chunks.append(" ".join(current_sentences))

    return chunks