# F:\Projects\HackathonOCR\backend\core\ocr\extraction_dla.py - EDITED

from typing import Dict, Any, List, Union
from backend.config.settings import settings
from backend.core.ocr.preprocessors import preprocess_image_pipeline
from backend.core.ocr.extraction_api import DeepSeekR1Extractor 
# We need PyMuPDF again to access image metadata.

# Initialize the DeepSeek Extractor instance 
try:
    # --- CRITICAL EDIT: Instantiate DeepSeekR1Extractor with NO arguments ---
    # It now pulls credentials and model name directly from the settings object.
    DEEPSEEK_EXTRACTOR = DeepSeekR1Extractor()
except Exception as e:
    DEEPSEEK_EXTRACTOR = None
    print(f"WARNING: DeepSeek Extractor not initialized. Check API key and settings. Error: {e}") 
    # Added error printing for better debugging

def _perform_document_layout_analysis(pdf_name: str, page_number: int) -> List[Dict[str, Any]]:
# ... (rest of the DLA placeholder function remains the same) ...
    if page_number == 1 and pdf_name == "socar.pdf":
        return [
            {"type": "figure", "bounding_box": [100, 200, 500, 600], "image_path": "temp/socar_p1_fig1.jpg"}
        ]
    return []


def process_page_for_ocr(page_data: Dict[str, Union[int, str, bytes]]) -> Dict[str, Union[int, str, bytes, bool, List[Dict]]]:
# ... (all logic below this line remains the same as it correctly uses the initialized DEEPSEEK_EXTRACTOR) ...
    """
    Orchestrates the full OCR process for a single page: preprocessing, DLA, and VLM OCR.
    """
    pdf_name = page_data["pdf_name"]
    page_number = page_data["page_number"]
    raw_image_bytes = page_data["original_image_bytes"]
    
    # 1. Image Preprocessing
    pipeline_keys = ["denoise", "binarization"] # Define which modular steps to run
    preprocessed_output = preprocess_image_pipeline(
        image_bytes=raw_image_bytes,
        pipeline_keys=pipeline_keys,
        pdf_name=pdf_name,
        page_number=page_number,
    )
    
    processed_image_bytes = preprocessed_output["processed_image_bytes"]
    saved_path = preprocessed_output["saved_path"]
    
    # 2. Document Layout Analysis (DLA) - extracts locations of non-text elements
    image_metadata = _perform_document_layout_analysis(pdf_name, page_number)
    
    # 3. VLM OCR Extraction
    if DEEPSEEK_EXTRACTOR:
        # Use the cleaned image bytes for maximum accuracy
        markdown_text = DEEPSEEK_EXTRACTOR.extract_markdown(processed_image_bytes)
    else:
        markdown_text = f"OCR_ERROR: API Extractor not available for page {page_number}"
        
    # 4. Final structured page result
    return {
        "page_number": page_number,
        "MD_text": markdown_text,
        "pdf_name": pdf_name,
        # Image/DLA Metadata is included here for the API response (if needed)
        "images_metadata": image_metadata, 
        # Debugging field
        "processed_image_path": saved_path,
        "is_successful": not markdown_text.startswith("OCR_ERROR"),
    }