from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

from agent.config import QDRANT_PATH
from agent.embeddings import get_embedding_model

COLLECTION_NAME = "documents"
client = None

def get_qdrant_client():
    global client
    if client is None:
        client = QdrantClient(path=str(QDRANT_PATH))
    return client

def close_qdrant():
    global client
    if client:
        client.close()
        client = None

def create_collection():
    client = get_qdrant_client()

    collections = client.get_collections()

    existing = [c.name for c in collections.collections]

    if COLLECTION_NAME in existing:
        return
    print(f"Creating collection '{COLLECTION_NAME}' in Qdrant...")
    print(f"Existing collections: {existing}")

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
    )

def get_vector_store():

    create_collection()

    client = get_qdrant_client()

    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=get_embedding_model()
    )