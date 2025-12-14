# F:\Projects\HackathonOCR\backend\api\router.py

import os
import shutil
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends

# --- Import Core Components ---
from backend.config.settings import settings
# NOTE: We need to assume these pipeline and model files exist outside the files we are rewriting
from backend.pipelines.ingestion_pipeline import run_document_ingestion
from backend.pipelines.vectorization_pipeline import run_vectorization_pipeline
from backend.core.rag.rag_chat_agent import RAGChatAgent, LLMResponse as CoreLLMResponse
# NOTE: We need to assume OCRResponse, LLMRequest, and LLMResponse Pydantic models are defined in backend.api.models
from backend.api.models import OCRResponse, LLMRequest, LLMResponse 

router = APIRouter()

# --- Dependency Injection: Initialize RAG Agent ---
# Define a dependency function to create the RAGChatAgent instance.
def get_rag_agent() -> RAGChatAgent:
    """Provides a RAGChatAgent instance for API endpoints."""
    # FastAPI's Depends() will handle caching/lifecycle based on the context
    return RAGChatAgent()

# Type alias for easy dependency injection annotation
RAGAgentDep = Annotated[RAGChatAgent, Depends(get_rag_agent)]

# ====================================================================
# 1. OCR ENDPOINT (Ingestion & Vectorization) - POST /api/v1/ocr
# ====================================================================

@router.post(
    "/ocr", 
    response_model=OCRResponse, 
    tags=["Ingestion"],
    summary="Upload PDF, run OCR, and index vectors."
)
async def ocr_and_index_document(file: UploadFile = File(...)):
    """
    Handles PDF upload, performs OCR to extract text, chunks the text, 
    generates embeddings, and upserts vectors into the Qdrant database.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    temp_file_path = settings.UPLOAD_FOLDER / file.filename
    print(f"Starting ingestion for file: {file.filename}")
    
    try:
        # 1. Save the file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Run the full OCR pipeline (VLM/OCR extraction)
        ocr_response = run_document_ingestion(str(temp_file_path))
        
        if "error" in ocr_response:
            raise HTTPException(status_code=500, detail=f"OCR Pipeline failed: {ocr_response['error']}")

        # 3. Run the Vectorization Pipeline (Chunking, Embedding, Qdrant Upsert)
        # This step uses the QdrantVectorDB, which might be in-memory if the connection failed.
        vector_success = run_vectorization_pipeline(ocr_response)

        if not vector_success:
            print(f"[WARNING] Vectorization failed for {file.filename}, but OCR results are available.")
        
        # 4. Return the OCR results
        return OCRResponse(**ocr_response)

    except Exception as e:
        print(f"Processing Error in /ocr endpoint: {e}")
        # Re-raise as HTTPException for user feedback
        raise HTTPException(status_code=500, detail=f"Internal server error during document processing: {e}")
        
    finally:
        # Clean up the temporary file
        if temp_file_path.exists():
            os.remove(temp_file_path)

# ====================================================================
# 2. LLM ENDPOINT (Retrieval Augmented Generation) - POST /api/v1/chat
# ====================================================================

@router.post(
    "/chat", 
    response_model=LLMResponse, 
    tags=["Chatbot"],
    summary="Ask a question and get a grounded answer with citations."
)
async def chat_with_document_agent(request: LLMRequest, agent: RAGAgentDep):
    """
    Receives a user question, uses the RAG agent to retrieve context from the 
    vector database, and generates a grounded answer.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Convert Pydantic ChatMessage list to the core RAG agent's internal dictionary format
    history_dicts = [h.model_dump() for h in request.history]
    
    # 1. Run the RAG generation logic
    core_response: CoreLLMResponse = agent.generate_response(
        query=request.question,
        history=history_dicts
    )

    # 2. Map the CoreLLMResponse (TypedDict) back to the Pydantic LLMResponse model
    return LLMResponse(**core_response)