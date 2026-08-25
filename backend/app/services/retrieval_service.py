import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from backend.app.services.embedding_service import load_faiss_index


from backend.app.config import (
    TOP_K,
    RELEVANCE_THRESHOLD,
    CHUNKS_FILE,
    FAISS_INDEX_FILE
)


model = SentenceTransformer("all-MiniLM-L6-v2")


def search_index(index, query_embedding, top_k=3):
    """
    Search the FAISS index and return the closest matching chunks.
    """
    distances, indices = index.search(query_embedding, top_k)

    return distances, indices


def save_chunks(chunks, file_path):
    """
    Save all chunks into a JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            chunks,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_chunks(file_path):
    """
    Load all saved chunks from JSON.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)





def retrieve_context(question: str, top_k: int = TOP_K):
    """
    Retrieve relevant chunks from FAISS.

    Returns:
        {
            "context": "...",
            "sources": [
                {
                    "filename": "...",
                    "chunk_id": ...,
                    "distance": ...
                }
            ]
        }

    Raises:
        RuntimeError: If retrieval infrastructure fails.
    """

    try:

        # --------------------------------------------------
        # Step 1: Generate embedding for the question
        # --------------------------------------------------

        query_embedding = model.encode([question])

        query_embedding = np.array(
            query_embedding
        ).astype("float32")

        # --------------------------------------------------
        # Step 2: Load FAISS index
        # --------------------------------------------------

        index = load_faiss_index(
            FAISS_INDEX_FILE
        )

        # --------------------------------------------------
        # Step 3: Search FAISS index
        # --------------------------------------------------

        distances, indices = search_index(
            index,
            query_embedding,
            top_k=top_k
        )

        print("FAISS distances:", distances)
        print("FAISS indices:", indices)

        # --------------------------------------------------
        # Step 4: Load chunks
        # --------------------------------------------------

        chunks = load_chunks(
            CHUNKS_FILE
        )

        retrieved_chunks = []

        sources = []

        # Keep track of duplicate text
        seen_chunks = set()

        # --------------------------------------------------
        # Step 5: Process FAISS results
        # --------------------------------------------------

        for distance, idx in zip(
            distances[0],
            indices[0]
        ):

            if idx == -1:
                print(
                    f"Rejected chunk {idx}"
                )
                continue

            if distance > RELEVANCE_THRESHOLD:
                print(
                    f"Rejected chunk {idx} "
                    f"with distance {distance}"
                )
                continue

            chunk = chunks[idx]

            # Extract text from metadata structure
            chunk_text = chunk["text"]

            # Avoid duplicate chunks
            if chunk_text in seen_chunks:

                print(
                    f"Skipped duplicate chunk {idx}"
                )

                continue

            print(
                f"Accepted chunk {idx} "
                f"from {chunk['filename']} "
                f"with distance {distance}"
            )

            # Add text to context
            retrieved_chunks.append(
                chunk_text
            )

            # Add source metadata
            sources.append(
                {
                    "filename": chunk["filename"],
                    "chunk_id": int(idx),
                    "distance": float(distance)
                }
            )

            seen_chunks.add(chunk_text)

        # --------------------------------------------------
        # Step 6: Combine chunks
        # --------------------------------------------------

        context = "\n\n".join(
            retrieved_chunks
        )

        # --------------------------------------------------
        # Step 7: Return context + source metadata
        # --------------------------------------------------

        return {
            "context": context,
            "sources": sources
        }

    except Exception as e:

        print("Retrieval Error:", e)

        raise RuntimeError(
            "Unable to retrieve information from the document store."
        ) from e