from langchain_community.vectorstores import FAISS

from agent.embeddings import get_embedding_model

def create_vector_store(chunks):

    embeddings = get_embedding_model()

    db = FAISS.from_texts(
        texts=chunks,
        embedding=embeddings
    )

    return db

def save_vector_store(db, path):
    db.save_local(path)

def load_vector_store(path):
    embeddings = get_embedding_model()

    return FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )