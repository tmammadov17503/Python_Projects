import os
from dataclasses import dataclass

@dataclass
class Settings:
    # Storage
    CHROMA_DIR: str = os.getenv("CHROMA_DIR", "./chroma_db")

    # PDF rasterization (pdf2image) – optional
    POPPLER_PATH: str | None = os.getenv("POPPLER_PATH")  # e.g. "C:\\poppler\\Library\\bin" or "/usr/bin"

    # Tesseract – optional
    TESSERACT_CMD: str | None = os.getenv("TESSERACT_CMD")  # e.g. "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    # OCR quality knobs
    PDF_DPI: int = int(os.getenv("PDF_DPI", "250"))
    OCR_MIN_TEXT_CHARS: int = int(os.getenv("OCR_MIN_TEXT_CHARS", "40"))

    # Embeddings
    EMBED_MODEL: str = os.getenv(
        "EMBED_MODEL",
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    # LLM (optional but recommended)
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

settings = Settings()
