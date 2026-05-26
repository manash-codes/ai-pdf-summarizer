import pymupdf
from langchain_core.documents import Document

class PDFLoader:

    @staticmethod
    def load(pdf_path: str) -> list[Document]:
        pdf = pymupdf.open(pdf_path)

        documents: list[Document] = []

        for page_number in range(len(pdf)):
            page = pdf[page_number]
            text = str(page.get_text("text"))

            if not text.strip():
                continue

            documents.append(
                Document(
                    page_content=text,
                    metadata={
                        "page": page_number + 1
                    }
                )
            )            
        return documents

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        doc = pymupdf.open(pdf_path)

        pages = []

        for page in doc:
            pages.append(page.get_text())
        
        return "\n".join(pages)