# PDF RAG Agent

A lightweight PDF retrieval-augmented generation (RAG) demo using OpenAI embeddings, FAISS, and FastAPI.

## Overview

This repository shows how to:
- extract text from PDF files with `pymupdf`
- split document text into chunks for embeddings
- create and persist a FAISS vector store
- retrieve relevant passages for a question
- generate an answer using OpenAI's `gpt-4.1-mini`
- expose a simple QA API with FastAPI

## Project structure

- `ingest.py` - extracts text from `data/sample.pdf`, chunks it, builds a FAISS index, and saves it to `data/faiss_index`
- `api/main.py` - FastAPI app that loads the vector store and responds to `/ask`
- `agent/pdf_loader.py` - PDF text extraction using `pymupdf`
- `agent/chunker.py` - text splitting using `langchain_text_splitters`
- `agent/vector_store.py` - FAISS index creation, saving, and loading
- `agent/embeddings.py` - OpenAI embedding model configuration
- `agent/retriever.py` - similarity search to retrieve relevant context
- `agent/qa.py` - formulates a prompt and calls OpenAI to answer questions
- `agent/summarizer.py` - document summarization support using OpenAI
- `agent/prompts/` - prompt templates for QA and summarization
- `agent/config.py` - environment and chunking configuration

## Requirements

- Python 3.12+
- OpenAI API key
- `faiss-cpu`
- `fastapi`, `uvicorn`
- `langchain`, `langchain-community`, `langchain-openai`, `langchain-text-splitters`
- `openai`
- `pydantic`
- `pymupdf`

Dependencies are defined in `pyproject.toml`.

## Setup

1. Create a Python environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install the package and dependencies:

```bash
python -m pip install -e .
```

3. Create a `.env` file in the repo root with your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_api_key
```

## Build the vector index

Run the ingestion script to extract the PDF text, split it into chunks, embed the chunks, and save the FAISS index:

```bash
python ingest.py
```

The index is saved under `data/faiss_index`.

## Run the API

Start the FastAPI service:

```bash
uvicorn api.main:app --reload
```

The server will load the saved FAISS index and expose a `/ask` endpoint.

## Ask a question

Send a POST request to `/ask` with JSON payload:

```json
{
  "question": "What is this document about?"
}
```

Example `curl` request:

```bash
curl -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d "{\"question\": \"What is this document about?\"}"
```

## Notes

- `main.py` is currently a placeholder entrypoint.
- The QA endpoint uses contextual retrieval from the FAISS store and delegates answer generation to OpenAI.
- The summarizer module can generate summaries from retrieved text but is not wired into the API by default.

## License

This project is released under the terms of the `LICENSE` file.
