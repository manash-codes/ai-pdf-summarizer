import json 
import shutil

from uuid import uuid4
from dataclasses import asdict
from pathlib import Path

from agent.config import UPLOADS_DIR, METADATA_DIR
from agent.models.document import DocumentMetadata

from agent.pdf_loader import PDFLoader
from agent.chunker import split_documents

from agent.qdrant_store import get_vector_store
from agent.utils.hash_utils import calculate_file_hash


class DocumentService:

    def generate_document_id(self):
        return str(uuid4())
    
    def metadata_path(self, document_id:str):
        return METADATA_DIR / f"{document_id}.json"
    
    def save_metadata(self, metadata: DocumentMetadata):
        with open(self.metadata_path(metadata.document_id), "w", encoding="utf-8") as file:
            json.dump(asdict(metadata), file, indent=2)

    def load_metadata(self, document_id:str):
        path = self.metadata_path(document_id)

        if not path.exists():
            return None
        
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
        
    def find_by_hash(self, file_hash:str):
        for file in METADATA_DIR.glob("*.json"):
            with open(file, "r", encoding="utf-8") as fp:
                data = json.load(fp)

                if(data["file_hash"] == file_hash):
                    return data
        return None
    
    def process_document(self, uploaded_file):
        print("Processing document:", uploaded_file)
        document_id = self.generate_document_id()
        destination = UPLOADS_DIR / f"{document_id}.pdf"
        
        source_path = Path(uploaded_file)

        shutil.copy(source_path, destination)

        file_hash = calculate_file_hash(str(destination))

        existing = self.find_by_hash(file_hash)

        if existing:
            return {
                "document_id": existing["document_id"],
                "status": "already_exists"
            }
        
        pages = PDFLoader.load(str(destination))
        chunks = split_documents(pages)

        for idx, chunk in enumerate(chunks):
            chunk.metadata["document_id"] = document_id
            chunk.metadata["chunk_id"] = idx

        vector_store = get_vector_store()

        vector_store.add_documents(chunks)

        metadata = DocumentMetadata.create(
            document_id=document_id,
            filename=destination.name,
            file_hash=file_hash,
            pages=len(pages),
            chunks=len(chunks)
        )
        
        self.save_metadata(metadata)
        
        print(f"Document {document_id} processed: {len(pages)} pages, {len(chunks)} chunks")
        return {
            "document_id": document_id,
            "pages": len(pages),
            "chunks": len(chunks),
            "status": "indexed"
        }

