from pathlib import Path

from agent.services.document_service import (
    DocumentService
)

service = DocumentService()


pdf_path = (
    Path(__file__)
    .parent.parent
    / "tests"
    / "sample.pdf"
)

print("PDF:", pdf_path)
print("Exists:", pdf_path.exists())


result = service.process_document(
    pdf_path
)

print(result)