from pydantic import BaseModel

class QueryRequest(BaseModel):
    file_id: str
    question: str
    top_k: int = 5