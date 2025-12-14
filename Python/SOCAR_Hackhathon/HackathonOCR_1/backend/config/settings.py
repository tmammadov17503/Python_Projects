# F:\Projects\HackathonOCR\backend\config\settings.py

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List

# Load environment variables from .env file (must be in the project root)
load_dotenv()

class Settings:
    """
    Central repository for all application settings, loaded from environment variables.
    """
    # --- Application & File Paths ---
    APP_NAME: str = os.getenv("APP_NAME", "SOCAR_RAG_SYSTEM")
    # Base folder for temporary file uploads
    UPLOAD_FOLDER: Path = Path(os.getenv("UPLOAD_FOLDER", "./temp_uploads"))
    
    # --- MODEL CONFIGURATION (Deployment IDs) ---
    OCR_MODEL_NAME: str = os.getenv("OCR_MODEL_NAME", "DeepSeek-R1")
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "Llama-4-Maverick-17B-128E-Instruct")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-3-large")

    # --- UNIFIED AZURE/OPENAI AUTHENTICATION ---
    # Full URL including the /openai/v1/ suffix for compatibility with openai client
    BASE_URL: str = os.getenv("BASE_URL", "") 
    API_KEY: str = os.getenv("API_KEY", "")
    # Removed EMBEDDING_ENDPOINT_ROOT as it was redundant with BASE_URL/EMBEDDING_MODEL_NAME

    # --- VECTOR DATABASE (Qdrant) ---
    QDRANT_HOST: str = os.getenv("QDRANT_HOST", "http://localhost:6333")
    QDRANT_API_KEY: str = os.getenv("QDRANT_API_KEY", "")

    # --- PREPROCESSING / DEBUGGING SETTINGS ---
    # Used for VLM/OCR processing
    APPLY_PREPROCESSING: bool = os.getenv("APPLY_PREPROCESSING", "True").upper() == "TRUE"
    OCR_PIPELINE_KEYS: List[str] = ["grayscale", "binarization", "denoise"]
    
    # Debug paths
    SAVE_PREPROCESSED_IMAGES: bool = os.getenv("SAVE_PREPROCESSED_IMAGES", "False").upper() == "TRUE"
    PREPROCESS_OUTPUT_DIR: Path = Path(os.getenv("PREPROCESS_OUTPUT_DIR", "./preprocessed_output"))

    def __init__(self):
        # Ensure the required directories exist upon initialization
        self.UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
        self.PREPROCESS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
# Instantiate settings for easy import throughout the application
settings = Settings()