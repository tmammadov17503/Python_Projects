# F:\Projects\HackathonOCR\backend\core\rag\rag_chat_agent.py

from typing import List, Dict, Any, TypedDict
from openai import OpenAI
from backend.config.settings import settings
from backend.core.embedding.embedding_api import EmbeddingAPIClient
from backend.core.vector_db.qdrant_client import QdrantVectorDB
from qdrant_client.http.models import ScoredPoint, SearchRequest # Added SearchRequest for clarity


# --- 1) Output structures ---

class SourceReference(TypedDict):
    """Structured data for a single retrieved source chunk."""
    pdf_name: str
    page_number: int
    content: str  # text of the retrieved chunk


class LLMResponse(TypedDict):
    """The final response structure returned by the RAG agent."""
    sources: List[SourceReference]
    answer: str


# --- 2) Core clients (shared singletons) ---
# These clients are instantiated once when the module loads
EMBEDDING_CLIENT = EmbeddingAPIClient()
QDRANT_CLIENT = QdrantVectorDB()


# --- 3) Utilities ---

def _qdrant_vector_search(
    client: QdrantVectorDB, # Type is the wrapper class
    collection_name: str,
    query_vector: List[float],
    top_k: int,
) -> List[ScoredPoint]:
    """
    Performs the vector search using the latest Qdrant API method available.
    """
    # The QdrantVectorDB exposes its client as `.client` for stability
    qdrant_core = client.client 
    
    if qdrant_core is None:
        # This should theoretically not happen if QdrantVectorDB init is successful
        raise RuntimeError("Qdrant client instance is None.")
    
    # Use the recommended modern `query_points` method
    # It handles both `query` and `query_vector` parameter names
    try:
        res = qdrant_core.query_points(
            collection_name=collection_name,
            query=query_vector, # Use the modern 'query' parameter
            limit=top_k,
            with_payload=True,
        )
        return getattr(res, "points", res) 
    
    except Exception as e:
        # Fallback to older search method if query_points fails unexpectedly
        print(f"Qdrant query_points failed ({type(e).__name__}). Falling back to search.")
        return qdrant_core.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            with_payload=True,
        )


# F:\Projects\HackathonOCR\backend\core\rag\rag_chat_agent.py

# ... (other code above) ...

def _safe_chat_completion(
        client: OpenAI,
        model: str,
        messages: List[Dict[str, str]],
        max_tokens_default: int = 512,
) -> str:
    """
    Call /chat/completions robustly across vendor variations using parameter fallbacks.
    Returns the assistant message text.
    """

    # We will try the most modern parameter name first and fallback if needed.
    params: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": 0.0,  # Use low temperature for fact-based RAG
    }

    # 1. Try max_completion_tokens (modern)
    try:
        resp = client.chat.completions.create(**params, max_completion_tokens=max_tokens_default)
        return resp.choices[0].message.content
    except Exception as e:
        msg = str(e)
        print(f"First attempt failed: {msg}. Trying legacy max_tokens...")

    # 2. Fallback to max_tokens (legacy/Azure specific)
    try:
        resp = client.chat.completions.create(**params, max_tokens=max_tokens_default)
        return resp.choices[0].message.content
    except Exception as e:
        # Update msg with the failure reason from the second attempt
        msg = f"{msg} | Legacy attempt failed: {e}"

    # Final failure
    # FIX: Remove 'from e' to resolve the 'cannot access local variable e' error.
    # The cause of the error is already captured in the 'msg' variable.
    raise RuntimeError(f"LLM chat completion failed after all attempts: {msg}")


# --- 4) RAG Agent ---

class RAGChatAgent:
    def __init__(self):
        # Initialize OpenAI client using settings (for LLM generation)
        self.client = OpenAI(
            api_key=settings.API_KEY,
            base_url=settings.BASE_URL,
        )
        self.llm_model_name = settings.LLM_MODEL_NAME

        self.qdrant_collection = QDRANT_CLIENT.COLLECTION_NAME
        self.top_k = 5

    def _retrieve_context(self, query: str) -> List[ScoredPoint]:
        """Embed the query and retrieve top_k chunks from Qdrant."""
        
        # 1. Get embedding for the user query
        query_embedding = EMBEDDING_CLIENT.get_embeddings([query])
        if not query_embedding:
            # This is the point where the RAG previously failed if EMBEDDING_CLIENT failed
            return []
        
        # 2. Run vector search using the global QDRANT_CLIENT instance
        return _qdrant_vector_search(
            client=QDRANT_CLIENT,
            collection_name=self.qdrant_collection,
            query_vector=query_embedding[0],
            top_k=self.top_k,
        )
    

    def _build_augmented_prompt(
        self,
        query: str,
        context_chunks: List[ScoredPoint],
        history: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        """
        Build the final message list for the LLM, including system instructions, context, 
        history, and the user query.
        """
        
        # Format retrieved chunks into a readable context block
        context_text = "\n\n".join([
            f"### Source: {s.payload.get('pdf_name','N/A')} (Page {s.payload.get('page_number','N/A')})\n"
            f"{s.payload.get('text','')}"
            for s in context_chunks if s.payload
        ])

        system_prompt = (
            "You are a SOCAR technical chat agent. Answer ONLY using the provided [CONTEXT].\n"
            "Rules:\n"
            "1) Use only facts from [CONTEXT]. If the answer is not found, say: "
            "\"I cannot find the answer in the provided documents.\"\n"
            "2) After each factual sentence, include a citation tag using this exact format: "
            ".\n"
            "3) Do not invent citations or use outside knowledge.\n\n"
            f"[CONTEXT]\n{context_text}\n\n[QUESTION]"
        )

        messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": query})
        
        return messages

    def generate_response(self, query: str, history: List[Dict[str, str]] | None = None) -> LLMResponse:
        """Execute RAG: retrieve, augment, generate, and package sources."""
        history = history or []

        # 1) Retrieve context
        context_chunks = self._retrieve_context(query)
        
        if not context_chunks:
            # This is the symptom observed when Qdrant was empty/volatile.
            return LLMResponse(
                sources=[],
                answer="I was unable to retrieve any relevant context from the knowledge base."
            )

        # 2) Build augmented prompt
        messages = self._build_augmented_prompt(query, context_chunks, history)

        # 3) Generate response
        try:
            raw_answer = _safe_chat_completion(
                client=self.client,
                model=self.llm_model_name,
                messages=messages,
                max_tokens_default=512,
            )
        except Exception as e:
            return LLMResponse(sources=[], answer=f"LLM API Error during generation: {e}")

        # 4) Collect and format sources for the final response
        sources: List[SourceReference] = []
        for s in context_chunks:
            payload = s.payload or {}
            sources.append(SourceReference(
                pdf_name=payload.get("pdf_name", "N/A"),
                page_number=payload.get("page_number", -1),
                content=payload.get("text", "N/A"),
            ))

        return LLMResponse(sources=sources, answer=raw_answer)