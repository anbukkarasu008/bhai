import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks: list[str]):
    """
    Generate embeddings for text chunks.
    """
    embeddings = model.encode(chunks)
    return embeddings


def create_faiss_index(embeddings):
    """
    Create a FAISS index and add embeddings.
    """
    embeddings = np.array(embeddings).astype("float32")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index


def save_faiss_index(index, file_path: str):
    """
    Save the FAISS index to disk.
    """
    faiss.write_index(index, file_path)

def load_faiss_index(file_path: str):
    """
    Load the FAISS index from disk.
    """
    return faiss.read_index(file_path)