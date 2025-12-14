# F:\Projects\HackathonOCR\backend\api\models.py

from pydantic import BaseModel, Field
from typing import List, Dict, Union, Optional

# --- 1. OCR Endpoint Response Models (5.1) ---

class OCRPageResponse(BaseModel):
    """Defines the structure for a single page's OCR output."""
    page_number: int = Field(..., description="The page index, starting from 1.")
    MD_text: str = Field(..., description="The Markdown-formatted extracted text for that page.")

class OCRResponse(BaseModel):
    """The final response model for the POST /ocr endpoint."""
    document_name: str
    pages: List[OCRPageResponse]


# --- 2. LLM Endpoint Request/Response Models (5.2) ---

class ChatMessage(BaseModel):
    """A standard message structure for user/assistant history."""
    role: str = Field(..., description="Role of the message sender ('user' or 'assistant').")
    content: str = Field(..., description="The message content.")

class LLMRequest(BaseModel):
    """The input model for the POST /chat endpoint."""
    question: str = Field(..., description="The user's current query.")
    history: List[ChatMessage] = Field(default_factory=list, description="Previous conversation turns for context awareness.")

class SourceReference(BaseModel):
    """Defines the structure for a single source citation."""
    pdf_name: str
    page_number: int
    content: str = Field(..., description="The relevant extracted text snippet (citation content).")

class LLMResponse(BaseModel):
    """The final response model for the POST /chat endpoint."""
    sources: List[SourceReference]
    answer: str = Field(..., description="The generated answer to the user query.")