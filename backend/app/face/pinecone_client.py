from pinecone import Pinecone, ServerlessSpec
from django.conf import settings


class PineconeClient:
    """A client to interact with Pinecone."""

    def __init__(self):
        """Initialize Pinecone client and ensure the index exists."""
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = "dev-face-encodings"
        self.dimension = 128  # Assuming face encodings are 128-dimensional
        self.metric = "cosine"
        self.index = self.pc.Index(self.index_name)

    def upsert_face_encoding(self, user_id, encoding):
        """Upsert a face encoding into the Pinecone index."""
        index = self.index
        vector = {
            "id": user_id,
            "values": encoding,
        }
        index.upsert(vectors=[vector])
        
    def query_face_encoding(self, encoding, top_k=1):
        """Query Pinecone index to find the closest face encodings."""
        index = self.index
        return index.query(vector=encoding, top_k=top_k, include_metadata=True)
