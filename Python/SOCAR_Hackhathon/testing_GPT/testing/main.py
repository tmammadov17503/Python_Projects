from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import traceback
from app.ocr_engine import OCREngine
from app.rag_engine import RAGEngine
from app.chatbot_engine import ChatbotEngine

app = FastAPI(title="SOCAR OCR API")

print("--- SYSTEM STARTUP ---")
ocr_engine = OCREngine()
rag_engine = RAGEngine()
chat_engine = ChatbotEngine(rag_engine)  # ✅ shared instance
print("--- SYSTEM READY ---")


@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        content = await file.read()

        # 1) OCR
        results = ocr_engine.process_pdf(content, mode="auto")

        # 2) Save to retriever (DO NOT let this crash the endpoint)
        try:
            rag_engine.add_document(file.filename, results)
        except Exception as db_e:
            print("❌ DB/Indexing failed:", repr(db_e))
            print(traceback.format_exc())
            # Still return OCR results so /ocr succeeds
            return {
                "warning": f"Indexing failed: {type(db_e).__name__}: {db_e}",
                "pages": results
            }

        return results

    except Exception as e:
        print("❌ OCR endpoint failed:", repr(e))
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {e}")



class Message(BaseModel):
    role: str
    content: str


@app.post("/chat")
async def chat_endpoint(history: List[Message]):
    history_dict = [{"role": m.role, "content": m.content} for m in history]
    return chat_engine.query(history_dict)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
