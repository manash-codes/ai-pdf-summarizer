from dataclasses import dataclass
from datetime import datetime

@dataclass
class DocumentMetadata:
    document_id: str
    filename: str
    file_hash: str
    pages: int
    chunks: int
    upload_time: str

    @classmethod
    def create(cls, document_id: str, filename:str, file_hash: str, pages: int, chunks: int):
        return cls(
            document_id=document_id,
            filename=filename,
            file_hash=file_hash,
            pages=pages,
            chunks=chunks,
            upload_time=datetime.utcnow().isoformat()
        )