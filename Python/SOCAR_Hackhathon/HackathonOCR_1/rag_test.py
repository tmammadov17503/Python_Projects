import os
import time
from typing import List, Dict, Any, Union, TypedDict
from openai import OpenAI, AzureOpenAI
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, VectorParams, ScoredPoint, PointStruct

# --- 1. CONFIGURATION (DEFINE YOUR ENVIRONMENT VARIABLES HERE) ---

# Replace these with your actual values (set them as environment variables or directly here)
API_KEY = os.environ.get("API_KEY")
BASE_URL = os.environ.get("BASE_URL", "https://llmapihackathon.services.ai.azure.com/openai/v1/")
EMBEDDING_MODEL_NAME = os.environ.get("EMBEDDING_MODEL_NAME", "text-embedding-3-large")
LLM_MODEL_NAME = os.environ.get("LLM_MODEL_NAME", "gpt-5") # Use your actual LLM Deployment ID

COLLECTION_NAME = "socar_test_knowledge"
EMBEDDING_DIMENSIONS = 3072
TOP_K = 3

if not API_KEY:
    raise RuntimeError("FATAL: API_KEY environment variable not set.")

# --- 2. Simplified Qdrant Wrapper (Mocks QdrantVectorDB) ---

class MockQdrantVectorDB:
    """Mocks the QdrantVectorDB class for a standalone test."""
    
    COLLECTION_NAME: str = COLLECTION_NAME
    VECTOR_SIZE: int = EMBEDDING_DIMENSIONS
    
    def __init__(self):
        # Initialize Qdrant in-memory client
        self.client = QdrantClient(location=":memory:") 
        
        # Ensure collection exists (Mocks the app startup logic)
        if not self.client.collection_exists(collection_name=self.COLLECTION_NAME):
            self._create_collection()
            
    def _create_collection(self):
        print(f"DEBUG: Creating Qdrant in-memory collection: {self.COLLECTION_NAME}")
    
        if self.client.collection_exists(self.COLLECTION_NAME):
            self.client.delete_collection(self.COLLECTION_NAME)
    
        self.client.create_collection(
            collection_name=self.COLLECTION_NAME,
            vectors_config=VectorParams(size=self.VECTOR_SIZE, distance=Distance.COSINE),
        )
    

# --- 3. Embedding Client (Mocks EmbeddingAPIClient) ---

class EmbeddingClient:
    """
    Implements the working configuration for Azure Embeddings.
    (Generic OpenAI client + Full BASE_URL).
    """
    def __init__(self):
        # FIX: Use generic OpenAI client with the full BASE_URL
        self.client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
        )
        self.model_name = EMBEDDING_MODEL_NAME

    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            response = self.client.embeddings.create(
                model=self.model_name,
                input=texts,
                dimensions=EMBEDDING_DIMENSIONS,
            )
            embeddings = sorted(response.data, key=lambda x: x.index)
            return [e.embedding for e in embeddings]
        except Exception as e:
            print(f"❌ EMBEDDING API ERROR: {e}")
            return []

# --- 4. RAG Agent Core Logic ---

class RAGAgent:
    
    def __init__(self, qdrant_db: MockQdrantVectorDB, embedding_client: EmbeddingClient):
        # --- FIX 1: Store the actual QdrantClient instance directly ---
        self.qdrant_core_client = qdrant_db.client
        # -----------------------------------------------------------
        self.embedding_client = embedding_client
        self.qdrant_collection = qdrant_db.COLLECTION_NAME
        self.top_k = TOP_K

        # Initialize the LLM Client (Use AzureOpenAI here as it's typically required for chat)
        # ✅ Use OpenAI-compatible client (same style as embeddings)
        self.llm_client = OpenAI(
            api_key=API_KEY,
            base_url=BASE_URL,
        )
        self.llm_model_name = LLM_MODEL_NAME
        
        
    def ingest_data(self, chunks: List[Dict[str, Any]]):
        """Generates embeddings and uploads points to Qdrant."""
        print("--- Starting Ingestion (Embedding and Upsert) ---")
        texts = [c['text'] for c in chunks]
        embeddings = self.embedding_client.get_embeddings(texts)
        
        if not embeddings:
            print("FAILURE: Could not generate embeddings. Aborting ingestion.")
            return

        points = [
            PointStruct(
                id=i + 1,
                vector=embeddings[i],
                payload=chunks[i]
            )
            for i in range(len(chunks))
        ]
        
        # --- FIX 2: Use the direct client attribute ---
        self.qdrant_core_client.upsert(
            collection_name=self.qdrant_collection,
            points=points,
            wait=True,
        )
        print(f"✅ SUCCESS: Uploaded {len(points)} vectors to Qdrant.")

    def _retrieve_context(self, query: str):
        """Converts query to vector and retrieves top_k relevant chunks."""
        query_embedding = self.embedding_client.get_embeddings([query])
        if not query_embedding:
            return []
    
        v = query_embedding[0]
        client = self.qdrant_core_client
    
        # ✅ Newer qdrant-client API
        if hasattr(client, "query_points"):
            try:
                res = client.query_points(
                    collection_name=self.qdrant_collection,
                    query=v,                 # vector
                    limit=self.top_k,
                    with_payload=True,
                )
            except TypeError:
                # Some versions use query_vector instead of query
                res = client.query_points(
                    collection_name=self.qdrant_collection,
                    query_vector=v,
                    limit=self.top_k,
                    with_payload=True,
                )
    
            # Some versions return an object with .points, others return list directly
            return getattr(res, "points", res)
    
        # ✅ Older qdrant-client API fallback (if present)
        if hasattr(client, "search"):
            return client.search(
                collection_name=self.qdrant_collection,
                query_vector=v,
                limit=self.top_k,
                with_payload=True,
            )
    
        raise RuntimeError(
            f"No compatible vector search method found. Client type: {type(client)}"
        )

    def generate_response(self, query: str) -> str:
        """Executes RAG chain to generate an answer."""
        
        # 1. Retrieve Context
        context_chunks = self._retrieve_context(query)
        if not context_chunks:
            return "I was unable to retrieve any relevant context from the knowledge base."

        # 2. Build Augmented Prompt (Simplified for standalone test)
        context_text = "\n\n".join([
            f"Source: {s.payload.get('file', 'N/A')} (Page {s.payload.get('page', 'N/A')})\n{s.payload.get('text')}"
            for s in context_chunks if s.payload
        ])
        
        system_prompt = f"""
        You are an intelligent technical chat agent. Answer the question based ONLY on the provided context.
        If the answer is not present in the context, state, "The answer is not available in the documents."
        
        [CONTEXT]:
        {context_text}
        
        [QUESTION]: {query}
        """
        messages = [{"role": "system", "content": system_prompt}]

        # 3. Generate Response
        try:
            print("\n--- Calling LLM for response generation... ---")
            completion = self.llm_client.chat.completions.create(
                model=self.llm_model_name,
                messages=messages,
                max_completion_tokens=512
            )
            return completion.choices[0].message.content

        except Exception as e:
            return f"❌ LLM API Error during generation: {e}"

# --- 5. Main Execution Block ---

def main():
    print("--- Starting Standalone RAG Test Module ---")

    # Sample data that would normally come from PDF chunking
    sample_data = [
        {"file": "DocA.pdf", "page": 1, "text": "Aşağı Kür çökəkliyində yüksək sürətli süxur çöküntüsü müşahidə edilir."},
        {"file": "DocA.pdf", "page": 1, "text": "Neft-qazlılıq əsasən Alt Horizontlarda cəmləşir, qərb bortları isə daha az məhsuldardır."},
        {"file": "DocB.pdf", "page": 3, "text": "Seysmik-geoloji təhlillər göstərir ki, Abşeron yarımadasında yeni kəşfiyyat sahələri mövcuddur."},
        {"file": "DocB.pdf", "page": 4, "text": "Məhsuldar Qatı Alt Horizontlar dərin qazma üçün əsas hədəfdir."}
    ]

    # Initialize components
    qdrant_db = MockQdrantVectorDB()
    embedding_client = EmbeddingClient()
    rag_agent = RAGAgent(qdrant_db, embedding_client)

    # Step 1: Ingest Data
    rag_agent.ingest_data(sample_data)

    # Step 2: Test Retrieval and Generation
    test_query = "Neft-qazlılıq harada cəmləşir?"
    print(f"\n--- Test Query: {test_query} ---")
    
    final_answer = rag_agent.generate_response(test_query)

    print("\n=============================================")
    print(f"FINAL RAG ANSWER:\n{final_answer}")
    print("=============================================")

if __name__ == "__main__":
    main()