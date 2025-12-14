# F:\Projects\HackathonOCR\run_demo.py - FINAL DEBUG VERSION WITH JSON SAVING

import json
import os
from pathlib import Path 
from backend.pipelines.ingestion_pipeline import run_document_ingestion
from backend.config.settings import settings # Ensures all settings and paths are initialized

# Define the PDF file path
# NOTE: Replace this path with the actual location of your file on your F: drive
PDF_FILE_PATH = "F:\\Projects\HackathonOCR\\hackathon_data\\test.pdf"

# =========================================================================
# --- NEW CONFIGURATION FLAG ---
# Set this to True to save the final JSON response to a file.
# The file will be saved in the 'output' directory in the project root.
SAVE_JSON_TO_FILE = True 
# =========================================================================

def mock_deepseek_extractor_output(page_number: int) -> str:
# ... (mock_deepseek_extractor_output remains the same) ...
    """Mocks the DeepSeek-R1 Markdown response for demonstration purposes."""
    if page_number == 1:
        # Corrected multiline string literal
        return (
            "## Исследование метаморфизма\n\n**1. Введение:** SOCAR обладает десятилетиями ценных исторических "
            "документов. Эти данные в основном представлены в рукописном виде и в печатных "
            "форматах на разных языках и скриптах.\n\n### 1.1 Problem Statement\n\n"
            "* Knowledge is not easily accessible, searchable, or analyzable.\n"
            "* The project aims to digitize valuable institutional knowledge."
        )
    elif page_number == 2:
        # Corrected multiline string literal
        return (
            "## Core Components\n\n1. OCR (Optical Character Recognition) Processing Module\n"
            "   - Process PDF documents containing handwritten and/or printed text\n"
            "   - Handle multiple alphabets, such as Azerbaijani (Cyrillic) / Russian\n\n"
            "2. Knowledge Base Creation\n\n* Store processed information in a searchable format."
        )
    else:
        return f"## Page {page_number} Continuation\n\nContent extracted successfully via DeepSeek R1."

# Overwrite the actual DeepSeek call with the mock data for local testing
class MockDeepSeekR1Extractor:
    def __init__(self):
        pass
    def extract_markdown(self, image_bytes: bytes) -> str:
        # We need the page number to return the correct mock content. 
        global MOCK_PAGE_COUNTER
        MOCK_PAGE_COUNTER += 1
        return mock_deepseek_extractor_output(MOCK_PAGE_COUNTER)

# Inject the mock class into the extraction_dla module for execution
MOCK_PAGE_COUNTER = 0
import importlib
import sys
try:
    # Attempt to import the required module for the patch
    module_name = 'backend.core.ocr.extraction_dla'
    if module_name in sys.modules:
        extraction_dla = sys.modules[module_name]
    else:
        extraction_dla = importlib.import_module(module_name)
    
    # --- CRITICAL EDIT: Check unified settings.API_KEY and use no-argument constructor ---
    if settings.API_KEY == "YOUR_AZURE_API_KEY_HERE":
        print("WARNING: Using Mock DeepSeek Extractor. No real API call will be made.")
        # Apply the patch with the no-argument constructor
        extraction_dla.DEEPSEEK_EXTRACTOR = MockDeepSeekR1Extractor()
    
except ImportError as e:
    print(f"Error during mock setup: {e}. Ensure all modules are correctly named and paths are set.")


if __name__ == "__main__":
    if not os.path.exists(PDF_FILE_PATH):
        print(f"ERROR: PDF file not found at: {PDF_FILE_PATH}")
        print("Please update PDF_FILE_PATH in run_demo.py to match your local file location.")
    else:
        # Run the full pipeline
        final_response = run_document_ingestion(PDF_FILE_PATH)

        # Print the final JSON structure for the OCR Endpoint
        print("\n--- Final OCR Endpoint JSON Response (Structure) ---")
        # Ensure the printed JSON is pretty and handles non-ASCII characters (Cyrillic)
        json_output_string = json.dumps(final_response, indent=2, ensure_ascii=False)
        print(json_output_string)

        # --- NEW JSON SAVING LOGIC ---
        if SAVE_JSON_TO_FILE:
            # Create a dedicated output directory
            OUTPUT_DIR = Path.cwd() / "output"
            OUTPUT_DIR.mkdir(exist_ok=True)
            
            # Use the PDF name to create a unique JSON file name
            pdf_name_stem = Path(PDF_FILE_PATH).stem
            json_file_path = OUTPUT_DIR / f"{pdf_name_stem}_ocr_output.json"
            
            try:
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    f.write(json_output_string)
                print(f"\n[SUCCESS] Final JSON saved to: {json_file_path}")
            except Exception as e:
                print(f"[ERROR] Could not save final JSON to file: {e}")
        # -----------------------------

        # Print the debugging information
        print(f"\n--- Debugging Output ---")
        print(f"Preprocessed images saved to the directory: {settings.PREPROCESS_OUTPUT_DIR}")
        print(f"Check this folder for the quality of your images before they were sent to DeepSeek.")