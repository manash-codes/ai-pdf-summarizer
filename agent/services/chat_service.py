from agent.retriever import Retriever
from agent.qa import QAService

class ChatService:
    def __init__(self):
        self.retriever = Retriever()
        self.qa_service = QAService()

    def ask(self, document_id:str, question:str):

        retrieved = self.retriever.retrieve(document_id=document_id, question=question)
        docs = [doc for doc, _ in retrieved]

        context = "\n\n".join(doc.page_content for doc in docs)

        answer = self.qa_service.answer(context=context, question=question)

        sources = sorted(
            {
                page
                for doc in docs
                if (page := doc.metadata.get("page")) is not None
            }
        )

        return { "answer": answer, "sources": sources }
