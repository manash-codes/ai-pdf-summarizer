import pymupdf

class PDFLoader:

    @staticmethod
    def extract_text(pdf_path: str) -> str:
        doc = pymupdf.open(pdf_path)

        pages = []

        for page in doc:
            pages.append(page.get_text())
        
        return "\n".join(pages)