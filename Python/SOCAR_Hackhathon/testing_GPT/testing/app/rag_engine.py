import os
import json
import uuid
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Doc:
    page_content: str
    metadata: Dict[str, Any]


class RAGEngine:
    """
    Torch-free retriever (TF-IDF). Very stable on Windows and good for Azerbaijani.
    Persists chunks to ./rag_store/chunks.jsonl
    """
    def __init__(self, store_dir: str = "./rag_store"):
        self.store_dir = store_dir
        os.makedirs(self.store_dir, exist_ok=True)
        self.chunks_path = os.path.join(self.store_dir, "chunks.jsonl")

        self.docs: List[Doc] = []
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.matrix = None

        self._load_chunks()
        self._rebuild_index()

    # ----------------- persistence -----------------
    def _load_chunks(self):
        self.docs = []
        if not os.path.exists(self.chunks_path):
            return
        with open(self.chunks_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                self.docs.append(Doc(page_content=obj["text"], metadata=obj["meta"]))

    def _append_chunk(self, text: str, meta: dict):
        with open(self.chunks_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({"text": text, "meta": meta}, ensure_ascii=False) + "\n")
    # ----------------- chunking -----------------
    def _chunk_text(self, text: str, chunk_size: int = 900, overlap: int = 120) -> List[str]:
        """
        Simple stable chunker (no langchain). Preserves paragraphs as much as possible.
        """
        text = (text or "").strip()
        if not text:
            return []

        # split into paragraphs first
        paras = [p.strip() for p in text.split("\n\n") if p.strip()]
        merged = []
        buf = ""

        for p in paras:
            if len(buf) + len(p) + 2 <= chunk_size:
                buf = (buf + "\n\n" + p).strip()
            else:
                if buf:
                    merged.append(buf)
                buf = p

        if buf:
            merged.append(buf)

        # apply overlap using sliding window over merged chunks (character overlap)
        out = []
        for m in merged:
            if len(m) <= chunk_size:
                out.append(m)
            else:
                start = 0
                while start < len(m):
                    end = min(start + chunk_size, len(m))
                    out.append(m[start:end])
                    if end == len(m):
                        break
                    start = max(0, end - overlap)

        return out

    # ----------------- indexing/search -----------------
    def _rebuild_index(self):
        if not self.docs:
            self.vectorizer = None
            self.matrix = None
            return

        texts = [d.page_content for d in self.docs]

        # char ngrams are robust for Azerbaijani, typos, OCR noise
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1
        )
        self.matrix = self.vectorizer.fit_transform(texts)

    def add_document(self, pdf_name: str, pages: List[Dict[str, Any]]) -> int:
        """
        pages: [{page_number:int, MD_text:str}, ...]
        """
        added = 0
        for page in pages:
            page_num = int(page.get("page_number", 1))
            text = (page.get("MD_text") or "").strip()
            if not text:
                continue

            chunks = self._chunk_text(text)
            for idx, ch in enumerate(chunks):
                meta = {
                    "source": pdf_name,
                    "page": page_num,
                    "start_index": idx,
                    "chunk_id": str(uuid.uuid4())
                }
                self.docs.append(Doc(page_content=ch, metadata=meta))
                self._append_chunk(ch, meta)
                added += 1

        if added > 0:
            self._rebuild_index()
            print(f"Added {added} chunks (TF-IDF index rebuilt).")
        else:
            print("No text extracted to add.")
        return added

    def search(self, query: str, k: int = 5) -> List[Doc]:
        query = (query or "").strip()
        if not query or not self.docs or self.vectorizer is None or self.matrix is None:
            return []

        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.matrix).flatten()

        top_idx = np.argsort(-sims)[:k]
        results = [self.docs[i] for i in top_idx if sims[i] > 0]

        # Sort results for stable citation order (pdf, page, start_index)
        results.sort(key=lambda d: (
            d.metadata.get("source", ""),
            int(d.metadata.get("page", 1)),
            int(d.metadata.get("start_index", 0))
        ))
        return results

    def count(self) -> int:
        return len(self.docs)
