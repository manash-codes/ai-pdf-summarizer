from langchain_text_splitters import RecursiveCharacterTextSplitter

from agent.config import CHUNK_SIZE, CHUNK_OVERLAP

def split_text(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
        )
    
    return splitter.split_text(text)

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP 
    )

    return splitter.split_documents(documents)