# 📄 Document QA System (PDF RAG)

A backend-first **Retrieval-Augmented Generation (RAG)** system that allows users to upload PDF documents, extract text (including OCR for scanned PDFs), generate semantic embeddings, store them in a FAISS vector index, and query the document using a Large Language Model.

This project is built with a **student-friendly, cost-effective stack**, using **free-tier Google Gemini APIs**, and focuses on correctness, modularity, and extensibility.

## 🚀 Features

- Upload PDF documents via API or Streamlit client
- Automatic detection of **text-based vs scanned PDFs**
- OCR extraction using **EasyOCR** for image-based pages
- Text normalization and cleanup pipeline
- Semantic chunking of document content
- Embedding generation using **Google Gemini Embeddings**
- Vector storage and similarity search using **FAISS**
- Question answering over documents using **Gemini LLM**
- Source-aware answers with **page and chunk references**

## 🧱 Project Architecture (Current)

The system is implemented as a **backend-first RAG pipeline** with a thin Streamlit client for testing.

### High-level Flow

1. **PDF Upload**
   - User uploads a PDF via Streamlit or API
   - File is saved locally and assigned a `file_id`

2. **Document Ingestion**
   - Text extracted from text-based pages
   - Images extracted from scanned pages
   - OCR applied only where needed (EasyOCR)

3. **Text Processing**
   - Text normalization and cleanup
   - Semantic chunking with page + chunk metadata

4. **Embedding & Indexing**
   - Each chunk embedded using Gemini Embeddings
   - Stored in a FAISS index (one index per document)
   - Metadata stored alongside vectors

5. **Querying**
   - User asks a question with `file_id` (automatically taken from the file upload response from backend)
   - Query is embedded
   - FAISS retrieves top-K relevant chunks
   - Retrieved context sent to Gemini LLM
   - Answer returned with source references
## 📂 Project Structure

```text
document_qa_system/
│
├── app/
│   ├── main.py                  # FastAPI app entry point
│   │
│   ├── routes/
│   │   ├── ingest.py             # PDF ingestion endpoint
│   │   └── query.py              # Question answering endpoint
│   │
│   ├── services/
│   │   ├── pdf_loader.py         # Text/image extraction from PDFs
│   │   ├── ocr_service.py        # EasyOCR-based OCR processing
│   │   ├── text_normalizer.py    # Text cleanup and normalization
│   │   ├── semantic_chunker.py   # Chunking logic with metadata
│   │   ├── embed.py              # Gemini embedding utilities
│   │   ├── faiss_store.py        # FAISS index build/save/load
│   │   ├── retriever.py          # Vector similarity search
│   │   └── qa_llm.py             # Gemini-based answer generation
│   │
│   └── models/
│       └── query.py              # Pydantic request models
|       └── document.py           # Document Upload State for responsive UI and document tracking.
│
├── uploads/                      # Uploaded PDF files (auto created when folder is uploaded)
├── vector_store/                 # FAISS indexes + metadata (auto created when folder is processed)
├── venv/                         # Python virtual environment (local only)
├── .env                          # Environment variables (not committed)
└── app.py                        # Streamlit_app (test)
```

## 🚀 Usage

### 1. Upload PDF
- Open the Streamlit UI in your browser.
- Upload a PDF document.
- Click **Upload & Process** to ingest the document.
- The backend extracts text, creates embeddings, and stores them in a FAISS index.
- A unique `file_id` is generated and stored in session state.

### 2. Ask Questions
- After successful ingestion, a question input box appears.
- Enter a question related to the uploaded document.
- Click **Ask** to query the document.
- The system retrieves relevant chunks using FAISS and generates an answer using Gemini.

### 3. Answer & Sources
- The generated answer is displayed.
- Retrieved source chunks are shown with their associated metadata (page and chunk identifiers).
