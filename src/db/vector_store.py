import json
from typing import List, Dict, Any
from pathlib import Path

class VectorStore:
    """
    A class to manage a vector store for documents, allowing for storage, retrieval, and management of document embeddings.
    """
    def __init__(self, storage_path: str = "vector_store.json"):
        """
        Initializes the VectorStore with a specified storage path.

        :param storage_path: The path to the JSON file where documents are stored.
        """
        self.storage_path = storage_path
        self.documents: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        """
        Loads documents from the storage path if the file exists.
        """
        path = Path(self.storage_path)
        if path.exists():
            with open(self.storage_path, 'r') as f:
                self.documents = json.load(f)

    def save(self):
        """
        Saves the current list of documents to the storage path in JSON format.
        """
        with open(self.storage_path, 'w') as f:
            json.dump(self.documents, f)

    def add_document(self, content: str, embedding: List[float], metadata: Dict[str, Any]):
        """
        Adds a new document to the vector store and saves it.

        :param content: The content of the document.
        :param embedding: The embedding vector associated with the document.
        :param metadata: Additional metadata related to the document.
        """
        doc = {
            'content': content,
            'embedding': embedding,
            'metadata': metadata
        }
        self.documents.append(doc)
        self.save()

    def get_all_documents(self):
        return self.documents

    def clear(self):
        self.documents = []
        self.save()