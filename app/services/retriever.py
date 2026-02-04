# app/services/retriever.py
import faiss
import pickle
import numpy as np
from pathlib import Path

INDEX_DIR = Path("vector_store")

def load_faiss_index(file_id: str):
    index_path = INDEX_DIR / f"{file_id}.index"
    meta_path = INDEX_DIR / f"{file_id}_meta.pkl"

    if not index_path.exists() or not meta_path.exists():
        raise FileNotFoundError("Vector index not found for this file_id")

    index = faiss.read_index(str(index_path))

    with open(meta_path, "rb") as f:
        metadata = pickle.load(f)

    return index, metadata


def search_index(index, metadata, query_embedding, top_k=5):
    query_vector = np.array([query_embedding]).astype("float32")
    faiss.normalize_L2(query_vector)

    scores, indices = index.search(query_vector, top_k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        results.append({
            "score": float(score),
            "metadata": metadata[idx]
        })

    return results