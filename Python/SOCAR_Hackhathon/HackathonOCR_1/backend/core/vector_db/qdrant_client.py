# F:\Projects\HackathonOCR\backend\core\vector_db\qdrant_client.py

from typing import List
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from backend.config.settings import settings
from backend.core.embedding.embedding_api import EmbeddingAPIClient

# NOTE: Assuming TextChunk is defined in chunker_utils and is a Dict with 'vector', 'text', and 'metadata'
# We will define a simple type alias here for clarity, though it requires TextChunk from its source
TextChunk = dict 

class QdrantVectorDB:
    """
    Client for managing the Qdrant vector database collection, with a fallback 
    to in-memory mode if the persistent host is unreachable.
    """
    
    COLLECTION_NAME: str = "socar_historical_knowledge"

    def __init__(self):
        self.vector_dim = EmbeddingAPIClient.EMBEDDING_DIMENSIONS
        self.client = None
        
        # --- 1. PRIMARY ATTEMPT: Connect to Persistent Remote/Host ---
        try:
            print(f"Attempting to connect to Qdrant host at {settings.QDRANT_HOST}...")
            
            # The Qdrant client handles full URLs, simplifying the initialization logic
            # Use 'url' for standard remote connections, or 'host'/'port' if necessary.
            self.client = QdrantClient(
                url=settings.QDRANT_HOST,
                api_key=settings.QDRANT_API_KEY,
                timeout=5 # Global timeout
            )
            
            # Test connection by listing collections. This must pass for persistence.
            self.client.get_collections() 
            
            print("[SUCCESS] Successfully connected to external Qdrant host.")
            
        except Exception as e:
            # --- 2. FALLBACK: Catch ALL initialization/connection errors ---
            print(f"\n[WARNING] Qdrant external connection FAILED ({type(e).__name__}: {e}).")
            print("         Falling back to Qdrant in-memory mode. DATA WILL NOT PERSIST across restarts.")
            
            # Re-initialize client to use in-memory mode
            self.client = QdrantClient(
                location=":memory:"
            )

        # 3. Ensure the collection exists in the active client (either remote or in-memory)
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self):
        """Creates or recreates the vector collection with the correct dimensions."""
        
        if not self.client.collection_exists(collection_name=self.COLLECTION_NAME):
            print(f"Creating Qdrant collection: {self.COLLECTION_NAME}...")
            self.client.recreate_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=self.vector_dim, 
                    distance=Distance.COSINE
                ),
                timeout=20
            )
            print("Collection created successfully.")
        else:
            print(f"Qdrant collection '{self.COLLECTION_NAME}' already exists.")

    def upsert_chunks(self, chunks: List[TextChunk]) -> bool:
        """
        Uploads a batch of vectors and their payloads (chunks) into the Qdrant collection.
        """
        if not chunks:
            return True

        points = []
        for i, chunk in enumerate(chunks):
            # Using point construction that matches your original payload structure
            points.append(PointStruct(
                id=i, # Note: This ID needs to be unique. A hash of the text chunk might be better long term.
                vector=chunk["vector"],
                payload={
                    "text": chunk["text"],
                    **chunk["metadata"] 
                }
            ))

        try:
            self.client.upsert(
                collection_name=self.COLLECTION_NAME,
                points=points,
                wait=True
            )
            print(f"[SUCCESS] Uploaded {len(points)} vectors to Qdrant collection '{self.COLLECTION_NAME}'.")
            return True
        except Exception as e:
            print(f"[FATAL QDRANT ERROR] Failed to upsert data: {e}")
            return False