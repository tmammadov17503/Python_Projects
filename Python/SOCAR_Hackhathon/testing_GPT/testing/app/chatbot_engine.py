from typing import List, Dict, Any
from app.config import settings

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class ChatbotEngine:
    def __init__(self, rag_engine):
        # IMPORTANT: use the SAME rag_engine instance that /ocr uses
        self.rag = rag_engine

        self.client = None
        if settings.OPENAI_API_KEY and OpenAI is not None:
            self.client = OpenAI(
                api_key=settings.OPENAI_API_KEY,
                base_url=settings.OPENAI_BASE_URL
            )

    def _last_user_message(self, history: List[Dict[str, str]]) -> str | None:
        for m in reversed(history):
            if (m.get("role") or "").lower() == "user":
                return (m.get("content") or "").strip()
        return None

    def _history_context(self, history: List[Dict[str, str]], max_turns: int = 6) -> str:
        tail = history[-max_turns:]
        lines = []
        for m in tail:
            role = (m.get("role") or "user").lower()
            content = (m.get("content") or "").strip()
            if content:
                lines.append(f"{role.upper()}: {content}")
        return "\n".join(lines)

    def _format_sources(self, docs) -> list[dict]:
        sources = []
        for d in docs:
            sources.append({
                "pdf_name": d.metadata.get("source", "unknown"),
                "page_number": int(d.metadata.get("page", 1)),
                "content": (d.page_content[:160] + "...") if len(d.page_content) > 160 else d.page_content
            })

        # Order matters for scoring (citation order)
        sources.sort(key=lambda x: (x["pdf_name"], x["page_number"]))
        return sources

    def _extractive_answer(self, question: str, docs) -> str:
        if not docs:
            return "No relevant info found in the documents."

        # A decent non-LLM fallback: summarize by concatenating best chunks
        parts = []
        for d in docs[:4]:
            src = d.metadata.get("source", "unknown")
            page = d.metadata.get("page", 1)
            snippet = d.page_content.strip()
            if len(snippet) > 350:
                snippet = snippet[:350] + "..."
            parts.append(f"- ({src}, p.{page}) {snippet}")

        return f"Based on the retrieved document sections for: '{question}'\n\n" + "\n".join(parts)

    def _llm_answer(self, question: str, docs, history: List[Dict[str, str]]) -> str:
        # If no key, no client -> fallback
        if self.client is None:
            return self._extractive_answer(question, docs)

        # Build context for model
        context_blocks = []
        for d in docs[:6]:
            src = d.metadata.get("source", "unknown")
            page = d.metadata.get("page", 1)
            chunk = d.page_content.strip()
            context_blocks.append(f"[SOURCE={src} | PAGE={page}]\n{chunk}")

        context_text = "\n\n".join(context_blocks)
        hist = self._history_context(history, max_turns=6)

        system = (
            "You are a document QA assistant. Answer ONLY using the provided context.\n"
            "If the answer is not in context, say you can't find it.\n"
            "Prefer the same language as the user.\n"
            "When you use a fact, mention the source + page like (PDF, p.X)."
        )

        user = (
            f"Conversation:\n{hist}\n\n"
            f"Question:\n{question}\n\n"
            f"Context:\n{context_text}\n\n"
            "Write a clear answer and include citations like (filename.pdf, p.3)."
        )

        resp = self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            temperature=0.2,
        )
        return resp.choices[0].message.content.strip()

    def query(self, chat_history: list) -> Dict[str, Any]:
        if not chat_history:
            return {"answer": "No question asked.", "sources": []}

        question = self._last_user_message(chat_history)
        if not question:
            return {"answer": "No user question found.", "sources": []}

        docs = self.rag.search(question, k=5)
        if not docs:
            return {"answer": "No relevant info found.", "sources": []}

        answer = self._llm_answer(question, docs, chat_history)
        sources = self._format_sources(docs)

        return {"answer": answer, "sources": sources}
