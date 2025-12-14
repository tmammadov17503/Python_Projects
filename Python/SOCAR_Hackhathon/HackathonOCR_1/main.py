# F:\Projects\HackathonOCR\main.py

import uvicorn
from fastapi import FastAPI
from backend.api.router import router as api_router
from backend.config.settings import settings

# --- Application Metadata ---
APP_TITLE = settings.APP_NAME
APP_VERSION = "1.0.0"
APP_DESCRIPTION = """
**SOCAR Historical Document RAG System**

A complete solution transforming historical handwritten and printed documents into an interactive, 
searchable knowledge base using Azure LLMs and Qdrant.
The system implements a two-endpoint REST API: 
1. **OCR Endpoint:** Handles document ingestion and vector indexing (`/api/v1/ocr`).
2. **LLM Endpoint:** Provides RAG-based answers with source citations (`/api/v1/chat`).
"""

# Define OpenAPI tags for clear categorization
TAGS_METADATA = [
    {"name": "Ingestion", "description": "Operations for PDF upload, OCR extraction, and vector indexing."},
    {"name": "Chatbot", "description": "Retrieval Augmented Generation (RAG) for answering natural language queries."},
]


def create_app() -> FastAPI:
    """Initializes and configures the FastAPI application."""
    app = FastAPI(
        title=APP_TITLE,
        version=APP_VERSION,
        description=APP_DESCRIPTION,
        openapi_tags=TAGS_METADATA,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # 1. Mount the API router
    # All routes defined in router.py will be accessible under /api/v1
    app.include_router(api_router, prefix="/api/v1")
    
    # 2. Add application startup event
    @app.on_event("startup")
    async def startup_event():
        print(f"Application startup complete. RAG services initialized using settings: {settings.APP_NAME}")
        # NOTE: Core clients (Qdrant, Embedding) are initialized upon first import/class instantiation

    return app

app = create_app()


if __name__ == "__main__":
    # Command to run the application using Uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)