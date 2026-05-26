from agent.services.chat_service import ChatService
from agent.qdrant_store import close_qdrant

DOCUMENT_ID = (
    "f4376bc2-ca4a-4e59-976e-8d4641cc456f"
)

chat = ChatService()

try:

    result = chat.ask(
        question="Summarize document",
        document_id=DOCUMENT_ID,
    )

    print(result)

finally:

    close_qdrant()

print(result)