from typing import List, Dict, Any
import numpy as np
from src.api import embed_texts
from src.db.vector_store import VectorStore

class EmbedService:
    def __init__(self):
        self.vector_store = VectorStore()

    def embed_and_store(self, text: str, metadata: Dict[str, Any]) -> None:
        embedding = self.embed(text)
        self.vector_store.add_document(text, embedding, metadata)

    def embed(self, text: str) -> List[float]:        
        embeddings = embed_texts([text], 'document')['embeddings']
        return embeddings[0]

    def embed_query(self, query: str) -> List[float]:
        embeddings = embed_texts([query], 'query')['embeddings']
        return embeddings[0]

    def compute_similarity(self, query_embedding: List[float], doc_embedding: List[float]) -> float:
        return np.dot(query_embedding, doc_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
        )