from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid
from app.services.pdf_loader import extract_text_or_images
from app.services.ocr_service import run_ocr
from app.services.text_normalizer import TextNormalizer
from app.services.semantic_chunker import SemanticChunker
from app.services.embed import embed_chunks
from app.services.faiss_store import build_faiss_index,save_index
router = APIRouter(prefix="/document", tags=["document"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")


async def upload_pdf(file: UploadFile = File(...)):
    '''
    Docstring for upload_pdf
    
    :param file: Description
    :type file: UploadFile
    return_type: dict
    return_vals: {
        file_details,
        extracted_content,
    }
    '''
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDFs allowed")

    file_id = f"{uuid.uuid4()}.pdf"
    file_path = UPLOAD_DIR / file_id

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text_chunks, images = extract_text_or_images(file_path)

    ocr_text = run_ocr(images) if images else []

    normalizer = TextNormalizer()
    all_pages = text_chunks + ocr_text
    clean_pages = normalizer.normalize_pages(all_pages)
    chunker = SemanticChunker()
    semantic_chunks = chunker.chunk_pages(clean_pages)
    embeddings_list = embed_chunks(semantic_chunks)


    index, metadata = build_faiss_index(embeddings_list)
    save_index(index, metadata, name=file_id)


    total_chars = sum(len(chunk["text"]) for chunk in semantic_chunks)

    return {
        "file_details": {
            "file_id": file_id,
            "pages_with_text": len(text_chunks),
            "pages_with_ocr": len(ocr_text),
            "total_chars": total_chars,
        },
        "extracted_content": clean_pages,
    }