from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHUNK_SIZE=1000
CHUNK_OVERLAP=200

INDEX_PATH = "data/faiss_index"

BASE_DIR = Path(__file__).resolve().parent

STORAGE_DIR = BASE_DIR / "storage"
UPLOADS_DIR = STORAGE_DIR / "uploads"
METADATA_DIR = STORAGE_DIR / "metadata"

QDRANT_PATH = BASE_DIR / "qdrant_data"

EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4.1-mini"

TOP_K_RESULTS = 5

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)
QDRANT_PATH.mkdir(parents=True, exist_ok=True)