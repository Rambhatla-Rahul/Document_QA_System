# app/routes/query.py
from fastapi import APIRouter, HTTPException
from app.models.query import QueryRequest
from app.services.embed import embed_query
from app.services.retriever import load_faiss_index, search_index
from app.services.qa_llm import generate_answer

router = APIRouter(prefix="/query", tags=["query"])

@router.post("/")
def query_document(request: QueryRequest):
    try:
        index, metadata = load_faiss_index(request.file_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not indexed")

    query_embedding = embed_query(request.question)

    retrieved = search_index(
        index=index,
        metadata=metadata,
        query_embedding=query_embedding,
        top_k=request.top_k
    )

    context = "\n\n".join(
        chunk["metadata"]["text"] for chunk in retrieved
    )

    answer = generate_answer(context, request.question)

    return {
        "question": request.question,
        "answer": answer,
        "sources": retrieved
    }