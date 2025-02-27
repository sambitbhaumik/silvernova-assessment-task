from typing import List, Dict, Any
from src.db.vector_store import VectorStore
from src.operations.embed import EmbedService

class SearchEngine:
    def __init__(self) -> None:
        self.vector_store = VectorStore()
        self.embed_service = EmbedService()

    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_embedding = self.embed_service.embed_query(query)
        
        results = []
        for doc in self.vector_store.get_all_documents():
            similarity = self.embed_service.compute_similarity(
                query_embedding, 
                doc['embedding']
            )
            results.append({
                'content': doc['content'],
                'metadata': doc['metadata'],
                'similarity': similarity
            })

        # Sort by similarity and return top k results
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]