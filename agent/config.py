from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHUNK_SIZE=1000
CHUNK_OVERLAP=200

INDEX_PATH = "data/faiss_index"