# F:\Projects\HackathonOCR\backend\core\embedding\embedding_api.py

from typing import List
from openai import OpenAI 
from backend.config.settings import settings

class EmbeddingAPIClient:
    """
    Client for generating embedding vectors using the configured Azure/OpenAI deployment.
    It uses the generic OpenAI client configured with the full BASE_URL for Azure compatibility.
    """
    
    # Matches the dimension of 'text-embedding-3-large'
    EMBEDDING_DIMENSIONS: int = 3072

    def __init__(self):
        # 1. Validation check
        if not settings.BASE_URL or not settings.API_KEY:
            raise ValueError("Azure API credentials (BASE_URL and API_KEY) must be set in settings.")
            
        self.model_name = settings.EMBEDDING_MODEL_NAME

        # Initialize with generic OpenAI client and the full BASE_URL from settings
        self.client = OpenAI(
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL,
        )
        print(f"Embedding Client Initialized for model: {self.model_name}")

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generates embedding vectors for a batch of text strings by calling the API.

        Args:
            texts: A list of text chunks (strings) to be embedded.

        Returns:
            A list of embedding vectors (list of floats). Returns [] on failure.
        """
        if not texts:
            return []
            
        try:
            # Use the simple create call without complex query params
            response = self.client.embeddings.create(
                model=self.model_name,
                input=texts,
                dimensions=self.EMBEDDING_DIMENSIONS,
            )
            
            # Extract and order the embedding vectors
            embeddings = sorted(response.data, key=lambda x: x.index)
            
            return [e.embedding for e in embeddings]
            
        except Exception as e:
            print(f"FATAL EMBEDDING API ERROR: Failed to get embeddings. Check BASE_URL and API_KEY. Error: {e}")
            return []