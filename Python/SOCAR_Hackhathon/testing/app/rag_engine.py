import os
import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class RAGEngine:
    def __init__(self, persist_directory="./chroma_db"):
        """
        Initializes the Vector Database (ChromaDB).
        We use a local CPU-friendly embedding model: 'all-MiniLM-L6-v2'.
        It's fast, small, and open-source (Good for Hackathon points).
        """
        print("Initializing Vector Store (ChromaDB)...")

        # 1. Load Embedding Model (Runs on CPU)
        self.embedding_function = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        # 2. Initialize ChromaDB (Persistent storage)
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_function
        )
        print("Vector Store Ready.")

    def add_document(self, pdf_name: str, pages: list):
        """
        Takes OCR output and saves it into the database.

        Args:
            pdf_name: Name of the file (e.g., 'report.pdf')
            pages: List of dicts from OCR [{'page_number': 1, 'MD_text': '...'}]
        """
        print(f"Adding {pdf_name} to Knowledge Base...")

        # 1. Split text into chunks (better for search)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

        docs_to_add = []

        for page in pages:
            page_num = page['page_number']
            text = page['MD_text']

            # Skip empty pages
            if not text.strip():
                continue

            # Split page text into smaller chunks
            chunks = text_splitter.create_documents([text])

            # Add metadata to each chunk so we can cite it later
            for chunk in chunks:
                chunk.metadata = {
                    "source": pdf_name,
                    "page": page_num,
                    "id": str(uuid.uuid4())
                }
                docs_to_add.append(chunk)

        # 2. Add to ChromaDB
        if docs_to_add:
            self.vector_store.add_documents(docs_to_add)
            print(f"Successfully added {len(docs_to_add)} chunks.")
        else:
            print("No text found to add.")

    def search(self, query: str, k: int = 3):
        """
        Searches the database for text relevant to the query.
        """
        results = self.vector_store.similarity_search(query, k=k)
        return results

# --- TEST BLOCK ---
if __name__ == "__main__":
    # Test creating the DB
    rag = RAGEngine()
    print("RAG Engine Initialized.")