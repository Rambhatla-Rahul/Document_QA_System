from google import genai
import os



_client = None

def get_genai_client():
    global _client
    if _client is None:
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not set in environment")
        _client = genai.Client(api_key=api_key)
    return _client


def embed_chunks(chunk_list):
    client = get_genai_client()
    '''
    Docstring for embed_chunks
    
    :param chunk_list: {\n
                    "chunk_id": chunk_id,\n
                    "page": page_idx + 1,\n
                    "text": " ".join(current_chunk)\n
                }
    '''
    embeddings_list = []
    for chunk in chunk_list:
        result = client.models.embed_content(
            model="gemini-embedding-001",
            contents = chunk["text"]
        )
        embedding_vector = result.embeddings[0].values

        metadata = {
            "chunk_id":chunk["chunk_id"],
            "page":chunk["page"],
            "text":chunk["text"],
        }
        embeddings_list.append({
            "embedding":embedding_vector,
            "metadata":metadata,
        })
    return embeddings_list

def embed_query(text: str):
    client = get_genai_client()
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )
    return result.embeddings[0].values