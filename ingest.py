from agent.pdf_loader import PDFLoader
from agent.chunker import split_text
from agent.vector_store import (
    create_vector_store,
    save_vector_store,
)

text = PDFLoader.extract_text(
    "data/sample.pdf"
)

chunks = split_text(text)

db = create_vector_store(
    chunks
)

save_vector_store(
    db,
    "data/faiss_index"
)

print("Index created")