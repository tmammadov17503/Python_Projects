import os
import time
import pickle
import hashlib
from typing import List, Dict, Tuple, Any
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

class EnhancedRAGPipeline:
    def __init__(self, 
                 index_path: str = "faiss_index",
                 embeddings_model: str = "sentence-transformers/all-mpnet-base-v2",
                 chunk_size: int = 1024,
                 chunk_overlap: int = 256):
        self.index_path = index_path
        self.metadata_path = os.path.join(index_path, "faiss_metadata.pkl")
        self.embeddings_model_name = embeddings_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embeddings = None
        self.db = None
        self.metadata = {}
    
    def get_file_hash(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return None
        
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def get_documents_hash(self, file_paths: List[str]) -> str:
        combined_hash = hashlib.md5()
        for file_path in sorted(file_paths):
            file_hash = self.get_file_hash(file_path)
            if file_hash:
                combined_hash.update(f"{file_path}:{file_hash}".encode())
        return combined_hash.hexdigest()
    
    def load_documents(self, file_paths: List[str]) -> Tuple[List[Document], float]:
        documents = []
        start_time = time.time()
        
        supported_extensions = {'.txt', '.pdf'}
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue
                
            file_extension = os.path.splitext(file_path)[1].lower()
            
            if file_extension not in supported_extensions:
                print(f"Unsupported file format: {file_path}")
                continue
            
            try:
                if file_extension == '.txt':
                    loader = TextLoader(file_path, encoding="utf-8")
                elif file_extension == '.pdf':
                    loader = PyPDFLoader(file_path)
                
                file_docs = loader.load()
                for doc in file_docs:
                    doc.metadata['source_file'] = file_path
                    doc.metadata['file_type'] = file_extension[1:]
                    
                documents.extend(file_docs)
                print(f"Loaded {len(file_docs)} chunks from {os.path.basename(file_path)}")
                
            except Exception as e:
                print(f"Error loading {file_path}: {str(e)}")
        
        load_time = time.time() - start_time
        return documents, load_time
    
    def split_documents(self, documents: List[Document]) -> Tuple[List[Document], float]:
        start_time = time.time()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.chunk_overlap,
            length_function=len
        )
        
        docs = text_splitter.split_documents(documents)
        
        for i, doc in enumerate(docs):
            doc.metadata['chunk_id'] = i
            doc.metadata['chunk_size'] = len(doc.page_content)
        
        split_time = time.time() - start_time
        return docs, split_time
    
    def initialize_embeddings(self) -> float:
        start_time = time.time()
        
        if self.embeddings is None:
            self.embeddings = HuggingFaceEmbeddings(
                model_name=self.embeddings_model_name,
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
        
        init_time = time.time() - start_time
        return init_time
    
    def create_vector_store(self, docs: List[Document]) -> Tuple[FAISS, float]:
        start_time = time.time()
        
        if not docs:
            raise ValueError("No documents provided for vector store creation")
        
        db = FAISS.from_documents(docs, self.embeddings)
        
        creation_time = time.time() - start_time
        return db, creation_time
    
    def save_index(self, db: FAISS, docs_hash: str, num_documents: int) -> float:
        start_time = time.time()
        
        os.makedirs(self.index_path, exist_ok=True)
        
        db.save_local(self.index_path)
        
        metadata = {
            'docs_hash': docs_hash,
            'embeddings_model': self.embeddings_model_name,
            'chunk_size': self.chunk_size,
            'chunk_overlap': self.chunk_overlap,
            'num_documents': num_documents,
            'index_version': '2.0'
        }
        
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        
        self.metadata = metadata
        save_time = time.time() - start_time
        return save_time
    
    def load_existing_index(self) -> Tuple[bool, float]:
        start_time = time.time()
        
        if not os.path.exists(self.index_path) or not os.path.exists(self.metadata_path):
            return False, 0
        
        try:
            with open(self.metadata_path, 'rb') as f:
                self.metadata = pickle.load(f)
            
            if self.embeddings is None:
                self.initialize_embeddings()
            
            self.db = FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            load_time = time.time() - start_time
            return True, load_time
            
        except Exception as e:
            print(f"Could not load existing index: {e}")
            return False, 0
    
    def should_rebuild_index(self, file_paths: List[str]) -> bool:
        if not self.metadata:
            return True
        
        current_hash = self.get_documents_hash(file_paths)
        stored_hash = self.metadata.get('docs_hash')
        
        if current_hash != stored_hash:
            return True
        
        if (self.metadata.get('embeddings_model') != self.embeddings_model_name or
            self.metadata.get('chunk_size') != self.chunk_size or
            self.metadata.get('chunk_overlap') != self.chunk_overlap):
            return True
        
        return False
    
    def build_or_load_index(self, file_paths: List[str], timing_info: List[str]) -> Tuple[FAISS, Dict[str, Any]]:
        current_docs_hash = self.get_documents_hash(file_paths)
        
        loaded, load_time = self.load_existing_index()
        
        if loaded and not self.should_rebuild_index(file_paths):
            print(f"Loaded existing FAISS index ({self.metadata.get('num_documents', 'Unknown')} chunks)")
            timing_info.append(f"FAISS index loaded: {load_time:.2f} seconds")
            return self.db, self.metadata
        
        print("Building new FAISS index...")
        
        documents, load_time = self.load_documents(file_paths)
        timing_info.append(f"Document loading: {load_time:.2f} seconds")
        
        if not documents:
            raise ValueError("No documents could be loaded")
        
        docs, split_time = self.split_documents(documents)
        timing_info.append(f"Document splitting: {split_time:.2f} seconds")
        
        embed_init_time = self.initialize_embeddings()
        timing_info.append(f"Embeddings initialization: {embed_init_time:.2f} seconds")
        
        self.db, creation_time = self.create_vector_store(docs)
        timing_info.append(f"FAISS creation: {creation_time:.2f} seconds")
        
        save_time = self.save_index(self.db, current_docs_hash, len(docs))
        timing_info.append(f"FAISS index saved: {save_time:.2f} seconds")
        
        print(f"FAISS index created and saved ({len(docs)} document chunks)")
        
        return self.db, self.metadata
    
    def search_similar_documents(self, query: str, k: int = 3) -> List[Document]:
        if self.db is None:
            raise ValueError("Vector store not initialized")
        
        return self.db.similarity_search(query, k=k)
    
    def get_index_stats(self) -> Dict[str, Any]:
        if not self.metadata:
            return {"status": "No index loaded"}
        
        stats = {
            "status": "Index loaded",
            "num_documents": self.metadata.get('num_documents', 0),
            "embeddings_model": self.metadata.get('embeddings_model', 'Unknown'),
            "chunk_size": self.metadata.get('chunk_size', 'Unknown'),
            "chunk_overlap": self.metadata.get('chunk_overlap', 'Unknown'),
            "index_version": self.metadata.get('index_version', '1.0')
        }
        
        return stats
    
    def cleanup_index(self):
        try:
            if os.path.exists(self.index_path):
                import shutil
                shutil.rmtree(self.index_path)
            return True
        except Exception as e:
            print(f"Error cleaning up index: {e}")
            return False