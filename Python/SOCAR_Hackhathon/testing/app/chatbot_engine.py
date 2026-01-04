from app.rag_engine import RAGEngine


class ChatbotEngine:
    def __init__(self):
        self.rag = RAGEngine()

    def query(self, chat_history: list):
        if not chat_history:
            return {"answer": "No question asked.", "sources": []}

        last_message = chat_history[-1]['content']
        docs = self.rag.search(last_message, k=3)

        if not docs:
            return {"answer": "No relevant info found.", "sources": []}

        context_text = "\n".join([d.page_content[:300] for d in docs])
        answer = f"Based on the documents, here is the information for '{last_message}':\n\n{context_text}"

        sources_list = []
        for doc in docs:
            sources_list.append({
                "pdf_name": doc.metadata.get('source', 'unknown'),
                "page_number": doc.metadata.get('page', 1),
                "content": doc.page_content[:100] + "..."
            })

        return {"answer": answer, "sources": sources_list}