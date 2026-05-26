from uuid import uuid4

class SessionService:
    def __init__(self):
        self.sessions = {}

    def create_session(self):
        session_id = str(uuid4())

        self.sessions[session_id] = { "document_id": None, "chat_history":[] }
        return session_id
    
    def attach_document(self, session_id:str, document_id):
        self.sessions[session_id]["document_id"] = document_id

    def add_message(self, session_id:str, role:str, content:str):
        return self.sessions[session_id]["chat_history"].append({"role": role,"content": content})
    
    def get_chat_history(self, session_id: str):
        return self.sessions[session_id]["chat_history"]
    
    def get_document_id(self, session_id: str):
        return self.sessions[session_id]["document_id"]
    
    def add_exchange(self, session_id:str, user_message:str, assistant_message:str):
        self.sessions[session_id]["chat_history"].append({"user": user_message, "assistant": assistant_message})