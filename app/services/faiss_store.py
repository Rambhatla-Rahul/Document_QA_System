import faiss
import numpy as np
import pickle
from pathlib import Path

INDEX_DIR = Path("vector_store")
INDEX_DIR.mkdir(exist_ok=True)

def build_faiss_index(embeddings_list):
    vectors = [item["embedding"] for item in embeddings_list]
    metadata = [item["metadata"] for item in embeddings_list]

    vectors = np.array(vectors).astype("float32")

    faiss.normalize_L2(vectors)

    dim = vectors.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(vectors)

    return index, metadata

def save_index(index, metadata, name="documents"):
    faiss.write_index(index, str(INDEX_DIR / f"{name}.index"))

    with open(INDEX_DIR / f"{name}_meta.pkl", "wb") as f:
        pickle.dump(metadata, f)