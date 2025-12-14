import fitz # PyMuPDF
from typing import List, Dict, Union, Optional

def convert_pdf_to_initial_pages(
    pdf_path: str, 
    pdf_name: str, 
    dpi: int = 300
) -> List[Dict[str, Union[int, str, bytes]]]:
    """
    Converts a multi-page PDF into a list of image pages, preserving order
    and initializing the data structure for the pipeline.
    
    Args:
        pdf_path: Local path to the uploaded PDF file.
        pdf_name: Name of the original PDF file (e.g., "socar.pdf").
        dpi: Resolution to render the PDF pages at (300 DPI is standard for OCR).

    Returns:
        A list of dictionaries, one for each page, with raw image bytes.
    """
    pages_data = []
    
    try:
        doc = fitz.open(pdf_path) 
    except Exception as e:
        # Handle file opening or corruption errors gracefully
        print(f"Error opening PDF {pdf_name}: {e}")
        return []

    # Define the matrix for high-resolution rendering
    zoom_matrix = fitz.Matrix(dpi / 72, dpi / 72)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Render the page to a raw, high-resolution image
        pix = page.get_pixmap(matrix=zoom_matrix)
        
        # Convert pixmap to image bytes (JPEG format)
        raw_img_bytes = pix.tobytes(output="jpeg")
        
        # Initialize the modular data structure
        pages_data.append({
            "pdf_name": pdf_name,
            "page_number": page_num + 1, # Page numbers start at 1
            "MD_text": "", 
            
            # --- CRITICAL FIX: Renamed key to match expected pipeline key ---
            "raw_image_bytes": raw_img_bytes, 
            # -----------------------------------------------------------------
            
            "processed_image_bytes": raw_img_bytes # Initial processed data is the same as raw
        })
        
    doc.close()
    return pages_data