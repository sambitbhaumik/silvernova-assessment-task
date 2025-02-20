from typing import List
from api import embed_texts
import logging

logger = logging.getLogger('embed')

class EmbedService:

  def __init__(self):
    pass

  def embed(self, text: str) -> List[float]:
    embeddings = embed_texts([text], 'document')[0]

    return embeddings