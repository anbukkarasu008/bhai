import os
from pathlib import Path

from dotenv import load_dotenv


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

UPLOAD_FOLDER = BASE_DIR / "backend" / "uploads"

VECTOR_STORE_FOLDER = BASE_DIR / "backend" / "vector_store"

CHUNKS_FILE = VECTOR_STORE_FOLDER / "chunks.json"

FAISS_INDEX_FILE = VECTOR_STORE_FOLDER / "faiss_index.bin"


# --------------------------------------------------
# Groq configuration
# --------------------------------------------------

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "openai/gpt-oss-20b"


# --------------------------------------------------
# Retrieval configuration
# --------------------------------------------------

TOP_K = 3

RELEVANCE_THRESHOLD = 1.5


# --------------------------------------------------
# Conversation configuration
# --------------------------------------------------

MAX_HISTORY_MESSAGES = 10