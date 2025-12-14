import uuid
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


class RAGEngine:
    def __init__(self, persist_directory="./chroma_db"):
        print("Initializing Vector Store...")
        self.embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_function
        )

    def add_document(self, pdf_name: str, pages: list):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs_to_add = []

        for page in pages:
            text = page['MD_text']
            if not text.strip(): continue

            chunks = text_splitter.create_documents([text])
            for chunk in chunks:
                chunk.metadata = {
                    "source": pdf_name,
                    "page": page['page_number'],
                    "id": str(uuid.uuid4())
                }
                docs_to_add.append(chunk)

        if docs_to_add:
            self.vector_store.add_documents(docs_to_add)
            print(f"Added {len(docs_to_add)} chunks to DB.")
        else:
            print("No text extracted to add.")

    def search(self, query: str, k: int = 3):
        return self.vector_store.similarity_search(query, k=k)