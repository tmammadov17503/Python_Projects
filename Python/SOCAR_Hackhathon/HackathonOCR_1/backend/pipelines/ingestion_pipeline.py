# F:\Projects\HackathonOCR\backend\pipelines\ingestion_pipeline.py - EDITED

from typing import List, Dict, Union
import json
import os
from pathlib import Path
from backend.core.ocr.pdf_to_image import convert_pdf_to_initial_pages
from backend.core.ocr.extraction_dla import process_page_for_ocr
from backend.core.ocr.preprocessors import preprocess_image_pipeline # <-- NEW IMPORT
from backend.core.ocr.extraction_api import DeepSeekR1Extractor # <-- NEW IMPORT
from backend.config.settings import settings

# Instantiate the extractor once for efficiency
DEEPSEEK_EXTRACTOR = DeepSeekR1Extractor()


def run_document_ingestion(pdf_path: str) -> Dict[str, Union[str, List[Dict]]]:
    """
    Executes the end-to-end OCR and extraction pipeline for a given PDF file.
    
    Returns the structured JSON response as specified for the OCR endpoint.
    """
    pdf_name = os.path.basename(pdf_path)

    print(f"--- Starting Ingestion Pipeline for: {pdf_name} ---")
    
    print(f"1. Converting PDF to {settings.PREPROCESS_OUTPUT_DIR / Path(pdf_name).stem}...")

    # A. Module 1: PDF to Image Conversion & Initialization
    # DPI is set to 300 here, you may need to adjust this in pdf_to_image.py if compression alone fails
    pages_data = convert_pdf_to_initial_pages(pdf_path, pdf_name, dpi=300) 

    if not pages_data:
        return {"document_name": pdf_name, "error": "Failed to convert PDF to images."}

    # B. Module 2 & 3: Preprocessing and DeepSeek OCR
    final_pages_output = []
    
    for i, page_data in enumerate(pages_data):
        print(f"2. Processing Page {page_data['page_number']}...")
        
        raw_image_bytes = page_data["raw_image_bytes"]
        page_number = page_data["page_number"]

        # --- NEW PREPROCESSING LOGIC ---
        if settings.APPLY_PREPROCESSING:
            # Run the full preprocessing pipeline (compression, filters)
            processed_data = preprocess_image_pipeline(
                image_bytes=raw_image_bytes,
                pipeline_keys=settings.OCR_PIPELINE_KEYS, # Assumes this key exists or uses default list
                pdf_name=pdf_name,
                page_number=page_number,
            )
            image_to_extract_bytes = processed_data["processed_image_bytes"]
            processed_image_path = processed_data["saved_path"]
            print(f"DEBUG: Preprocessing applied. Image size before send: {len(image_to_extract_bytes) / 1024:.2f} KB")

        else:
            # Skip preprocessing and use the original raw bytes
            image_to_extract_bytes = raw_image_bytes
            processed_image_path = "N/A (Preprocessing Skipped)"
            print(f"DEBUG: Preprocessing skipped. Using raw image bytes. Size: {len(image_to_extract_bytes) / 1024:.2f} KB")
        # -------------------------------
        
        # Call the DeepSeek API directly (since it's a simple sequential call now)
        markdown_text = DEEPSEEK_EXTRACTOR.extract_markdown(image_to_extract_bytes)
        
        page_result = {
            "page_number": page_number,
            "processed_image_path": processed_image_path,
            "MD_text": markdown_text
        }
        
        # Format the result according to the final OCR Endpoint Specification
        final_pages_output.append({
            "page_number": page_result["page_number"],
            "MD_text": page_result["MD_text"], 
        })
        
        # --- Debugging Output for User Review ---
        print(f"   -> Image saved to: {page_result.get('processed_image_path', 'N/A')}")
        print(f"   -> Extracted MD: {page_result['MD_text'][:100]}...")
        
    print(f"--- Ingestion Pipeline Finished for {pdf_name} ---")

    # C. Final OCR Endpoint Response Structure
    return {
        "document_name": pdf_name,
        "pages": final_pages_output
    }