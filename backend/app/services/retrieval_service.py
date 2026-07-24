import faiss
import json

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
        json.dump(chunks, file, indent=4, ensure_ascii=False)

def load_chunks(file_path):
    """
    Load all saved chunks from JSON.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)