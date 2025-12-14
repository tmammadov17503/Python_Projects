# F:\Projects\HackathonOCR\backend\core\ocr\preprocessors.py - EDITED FOR COMPRESSION

import cv2
import numpy as np
from typing import Callable, Dict, List, Any, Union
from pathlib import Path

# Import settings from the new configuration module
from backend.config.settings import settings 

# Define the JPEG Quality constant (65 is a common trade-off for aggressive file size reduction)
JPEG_COMPRESSION_QUALITY = 65 
JPEG_PARAMS = [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_COMPRESSION_QUALITY]

# --- Preprocessor Functions (Modular and interchangeable) ---
# ... (All preprocessor functions: convert_to_grayscale, apply_adaptive_binarization, apply_median_denoise remain the same) ...
def convert_to_grayscale(image: np.ndarray) -> np.ndarray:
    """Converts a color image array to a grayscale array."""
    if len(image.shape) == 3 and image.shape[2] == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def apply_adaptive_binarization(image: np.ndarray) -> np.ndarray:
    """Applies Gaussian Adaptive Thresholding for sharp B&W conversion."""
    if len(image.shape) > 2:
        gray_image = convert_to_grayscale(image)
    else:
        gray_image = image

    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # Adaptive Thresholding: handles uneven illumination
    binary_image = cv2.adaptiveThreshold(
        blurred, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 
        2
    )
    return binary_image

def apply_median_denoise(image: np.ndarray) -> np.ndarray:
    """Applies Median Blur to remove salt-and-pepper noise."""
    return cv2.medianBlur(image, 3)

# Define the dictionary of available preprocessors
PREPROCESSORS: Dict[str, Callable[[np.ndarray], np.ndarray]] = {
    "grayscale": convert_to_grayscale,
    "binarization": apply_adaptive_binarization,
    "denoise": apply_median_denoise,
}

# --- Image Saving Logic ---

def _save_image_for_review(image_array: np.ndarray, pdf_name: str, page_number: int, suffix: str = "processed") -> str:
    """
    Saves the image array to a document-specific output directory, applying JPEG compression.
    Returns the relative path to the saved file.
    """
    
    # 1. Create the document-specific subdirectory (e.g., ./preprocessed_output/socar_pdf)
    doc_name_base = Path(pdf_name).stem 
    doc_output_dir = settings.PREPROCESS_OUTPUT_DIR / doc_name_base
    doc_output_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Define the filename (e.g., socar_pdf_page_001_processed.jpg)
    filename = f"{doc_name_base}_page_{page_number:03d}_{suffix}.jpg"
    file_path = doc_output_dir / filename
    
    # 3. Convert array to bytes and save - *** APPLIED COMPRESSION HERE ***
    if len(image_array.shape) == 2:
        # Handle grayscale/binary image saving
        _, buffer = cv2.imencode('.jpg', image_array, JPEG_PARAMS)
    else:
        # Handle color image saving (BGR format)
        _, buffer = cv2.imencode('.jpg', image_array, JPEG_PARAMS)
        
    try:
        file_path.write_bytes(buffer.tobytes())
        # Return a relative path or string representation for easy reference
        return str(file_path) 
    except Exception as e:
        print(f"Error saving image to {file_path}: {e}")
        return "ERROR_SAVING_IMAGE"


def preprocess_image_pipeline(
    image_bytes: bytes,
    pipeline_keys: List[str],
    pdf_name: str,
    page_number: int,
) -> Dict[str, Union[bytes, str]]:
    """
    Runs a raw image through a modular preprocessing pipeline and optionally saves it.
    
    Returns a dictionary containing the processed image bytes and the optional saved path.
    """
    # 1. Decode image bytes into an OpenCV numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    # Use IMREAD_COLOR to ensure we can apply filters even if the source is grayscale
    image_array = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 

    if image_array is None:
        raise ValueError("Could not decode image bytes for preprocessing.")
    
    # 2. Execute the modular pipeline
    processed_array = image_array
    for key in pipeline_keys:
        if key in PREPROCESSORS:
            processed_array = PREPROCESSORS[key](processed_array)
        else:
            print(f"Warning: Unknown preprocessor '{key}' skipped on page {page_number}.")

    # 3. Convert the final processed NumPy array back to image bytes - *** APPLIED COMPRESSION HERE ***
    if len(processed_array.shape) == 2:
        _, buffer = cv2.imencode('.jpg', processed_array, JPEG_PARAMS) 
    else:
        _, buffer = cv2.imencode('.jpg', processed_array, JPEG_PARAMS)
        
    processed_bytes = buffer.tobytes()
    
    # 4. Optional: Save the image for debugging/review
    saved_path = ""
    if settings.SAVE_PREPROCESSED_IMAGES:
        saved_path = _save_image_for_review(processed_array, pdf_name, page_number)
        
    return {
        "processed_image_bytes": processed_bytes,
        "saved_path": saved_path
    }