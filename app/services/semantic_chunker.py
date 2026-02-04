from typing import List, Dict
import nltk
import tiktoken

import nltk
from nltk.data import find

def ensure_punkt():
    try:
        find("tokenizers/punkt")
        find("tokenizers/punkt_tab")
    except LookupError:
        nltk.download("punkt")
        nltk.download("punkt_tab")

ensure_punkt()

class SemanticChunker:
    def __init__(
        self,
        max_tokens: int = 300,
        overlap_tokens: int = 50,
        model_name: str = "gpt-4o-mini"  # token estimation only
    ):
        self.max_tokens = max_tokens
        self.overlap_tokens = overlap_tokens
        self.tokenizer = tiktoken.encoding_for_model(model_name)

    def _count_tokens(self, text: str) -> int:
        return len(self.tokenizer.encode(text))

    def chunk_pages(self, pages: List[str]) -> List[Dict]:
        chunks = []
        chunk_id = 0

        for page_idx, page_text in enumerate(pages):
            sentences = nltk.sent_tokenize(page_text)

            current_chunk = []
            current_tokens = 0

            for sentence in sentences:
                sentence_tokens = self._count_tokens(sentence)

                if current_tokens + sentence_tokens > self.max_tokens:
                    chunks.append({
                        "chunk_id": chunk_id,
                        "page": page_idx + 1,
                        "text": " ".join(current_chunk)
                    })
                    chunk_id += 1

                    # overlap handling
                    overlap_text = " ".join(current_chunk)[-self.overlap_tokens:]
                    current_chunk = [overlap_text]
                    current_tokens = self._count_tokens(overlap_text)

                current_chunk.append(sentence)
                current_tokens += sentence_tokens

            if current_chunk:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page": page_idx + 1,
                    "text": " ".join(current_chunk)
                })
                chunk_id += 1

        return chunks