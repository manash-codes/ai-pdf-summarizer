def retrieve_context(db, question:str, k: int=4):
    docs = db.similarity_search(question, k=k)
    return "\n\n".join(doc.page_content for doc in docs)