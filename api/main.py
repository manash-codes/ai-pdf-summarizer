from fastapi import FastAPI
from pydantic import BaseModel

from dotenv import load_dotenv
import agent.config 
load_dotenv()
from agent.qa import answer_question
from agent.retriever import retrieve_context
from agent.vector_store import load_vector_store

app = FastAPI()

db = load_vector_store(
    "data/faiss_index"
)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(payload: QuestionRequest):
    context = retrieve_context(db, payload.question)
    answer = answer_question(context, payload.question)
    return {"answer": answer}
