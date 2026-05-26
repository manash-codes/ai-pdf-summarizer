from qdrant_client import models

from agent.config import TOP_K_RESULTS
from agent.qdrant_store import get_vector_store

class Retriever:

    def __init__(self):
        self.vector_store = get_vector_store()

    def retrieve(self, document_id:str, question:str, limit :int=TOP_K_RESULTS):
        results = self.vector_store.similarity_search_with_score(
            query=question,
            k=limit,
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.document_id",
                        match=models.MatchValue(value=document_id)
                    )
                ]
            )
        )
        return results

def retrieve_context(db, question:str, k: int=4):
    docs = db.similarity_search(question, k=k)
    return "\n\n".join(doc.page_content for doc in docs)