# F:\Projects\HackathonOCR\backend\core\embedding\chunker_utils.py

from typing import List, Dict, TypedDict, Optional, Union
    
# --- 1. Define the Structured Output (TypedDict for Clarity) ---
class TextChunk(TypedDict):
    """Defines the structure for a single chunk ready for embedding."""
    text: str                       # The actual text content to be embedded
    metadata: Dict[str, Union[str, int]] # Source context (file, page, section_id)
    vector: Optional[List[float]]   # Will be populated by the EmbeddingAPIClient

# --- 2. Define the Splitter Configuration ---
# Recursive splitters prioritize splitting by the first item, then the second, and so on.
MARKDOWN_SEPARATORS = [
    "\n#{1,6} ",  # Major Headings (e.g., #, ##, ###)
    "\n\n\n",     # Triple newlines (Paragraph break)
    "\n\n",       # Double newlines (Sentence break)
    ". ",         # Sentence ending
    " ",          # Fallback to spaces
]
CHUNK_SIZE = 1000  # Target number of characters per chunk
CHUNK_OVERLAP = 150 # Overlap to ensure context isn't lost at boundaries


def chunk_markdown_document(
    markdown_text: str,
    page_number: int,
    pdf_name: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP,
) -> List[TextChunk]:
    """
    Splits a single page of Markdown text into a list of semantically coherent TextChunks.
    
    NOTE: In a real implementation, this function would use a library 
    like langchain_text_splitters.RecursiveCharacterTextSplitter 
    configured with MARKDOWN_SEPARATORS. For this project's structure, 
    we define the signature here.
    """
    
    # --- Placeholder Implementation (Replace with actual splitter logic) ---
    
    # 1. Initialize the list of final chunks
    final_chunks: List[TextChunk] = []
    
    # 2. Simplistic Split for now (to keep the flow moving)
    current_text = markdown_text
    
    while len(current_text) > 0:
        chunk_text = current_text[:chunk_size]
        
        # 3. Create the TextChunk object with mandatory metadata
        final_chunks.append(TextChunk(
            text=chunk_text,
            metadata={
                "pdf_name": pdf_name,
                "page_number": page_number,
                "section": f"Chunk_{len(final_chunks) + 1}", # Placeholder section name
                "source": f"{pdf_name}_p{page_number}"
            },
            vector=None # Vector is calculated later
        ))
        
        # 4. Advance the text pointer (handling overlap)
        if len(current_text) > chunk_size:
            current_text = current_text[chunk_size - chunk_overlap:]
        else:
            current_text = ""
            
    # --- End of Placeholder Implementation ---
    
    print(f"DEBUG: Page {page_number} split into {len(final_chunks)} chunks.")
    return final_chunks