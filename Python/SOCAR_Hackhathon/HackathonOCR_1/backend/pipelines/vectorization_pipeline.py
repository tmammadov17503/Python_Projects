# F:\Projects\HackathonOCR\backend\pipelines\vectorization_pipeline.py

from typing import List, Dict, Union
import json
import itertools
from backend.core.embedding.chunker_utils import chunk_markdown_document, TextChunk
from backend.core.embedding.embedding_api import EmbeddingAPIClient
from backend.core.vector_db.qdrant_client import QdrantVectorDB

# Initialize clients once for efficiency
EMBEDDING_CLIENT = EmbeddingAPIClient()
QDRANT_CLIENT = QdrantVectorDB()

# Define a maximum batch size for the embedding model (Azure default is often 16 or 32)
# We choose 32 for a balance between speed and reliability.
BATCH_SIZE = 32 

def run_vectorization_pipeline(ocr_response: Dict[str, Union[str, List[Dict]]]) -> bool:
    """
    Orchestrates the chunking, embedding, and vector storage process for an OCR response.
    
    Args:
        ocr_response: The dictionary structure outputted by the OCR Ingestion Pipeline.
        
    Returns:
        True if the vectorization and storage were successful, False otherwise.
    """
    
    document_name = ocr_response.get("document_name", "unknown_document")
    pages = ocr_response.get("pages", [])
    
    if not pages:
        print(f"WARNING: No pages found in OCR response for {document_name}. Skipping vectorization.")
        return True

    all_chunks: List[TextChunk] = []

    # 1. Chunking Phase: Iterate through each page and generate text chunks
    print(f"\n--- Starting Chunking Phase for {document_name} ---")
    for page_data in pages:
        page_number = page_data["page_number"]
        markdown_text = page_data["MD_text"]
        
        # Only chunk non-error pages
        if "OCR_ERROR" not in markdown_text and not markdown_text.strip().startswith("[oxunmur:"):
             chunks = chunk_markdown_document(
                markdown_text=markdown_text,
                page_number=page_number,
                pdf_name=document_name
            )
             all_chunks.extend(chunks)
        else:
             print(f"Skipping page {page_number} due to OCR error/unreadable content.")


    if not all_chunks:
        print("No valid chunks generated. Vectorization halted.")
        return True # Processed successfully, but nothing to index

    # 2. Embedding and Upsert Phase: Process chunks in batches
    print(f"\n--- Starting Embedding and Upsert Phase (Total Chunks: {len(all_chunks)}) ---")
    
    success = True
    
    # Use itertools to split the list of chunks into smaller lists of BATCH_SIZE
    chunk_iterator = iter(all_chunks)
    while batch := list(itertools.islice(chunk_iterator, BATCH_SIZE)):
        
        # Extract text for the API call
        texts_to_embed = [chunk["text"] for chunk in batch]
        
        # A. Call Embedding API
        embeddings = EMBEDDING_CLIENT.get_embeddings(texts_to_embed)
        
        if not embeddings or len(embeddings) != len(texts_to_embed):
            print(f"[ERROR] Embedding failed for a batch of {len(texts_to_embed)} chunks. Stopping.")
            success = False
            break
            
        # B. Integrate embeddings back into the TextChunk structure
        chunks_to_upsert: List[TextChunk] = []
        for i, chunk in enumerate(batch):
            # Update the chunk with the calculated vector
            chunk["vector"] = embeddings[i] 
            chunks_to_upsert.append(chunk)

        # C. Call Qdrant Upsert
        if not QDRANT_CLIENT.upsert_chunks(chunks_to_upsert):
            print("[FATAL] Qdrant upsert failed. Stopping vectorization.")
            success = False
            break

    print(f"\n--- Vectorization Pipeline Finished ({'SUCCESS' if success else 'FAILURE'}) ---")
    return success