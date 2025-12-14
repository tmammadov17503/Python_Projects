from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

# Import our engines
from app.ocr_engine import OCREngine
from app.rag_engine import RAGEngine
from app.chatbot_engine import ChatbotEngine

app = FastAPI(title="SOCAR OCR API")

# Initialize Engines
print("--- SYSTEM STARTUP ---")
ocr_engine = OCREngine()
rag_engine = RAGEngine()
chat_engine = ChatbotEngine()
print("--- SYSTEM READY ---")


# --- OCR ENDPOINT ---
@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    try:
        content = await file.read()
        mode = "cyr" if "cyr" in file.filename.lower() else "lat"

        print(f"File: {file.filename} | Mode: {mode}")
        # 1. Run OCR
        results = ocr_engine.process_pdf(content, mode=mode)

        # 2. Save to DB
        rag_engine.add_document(file.filename, results)

        return results
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- CHATBOT ENDPOINT ---
class Message(BaseModel):
    role: str
    content: str


@app.post("/chat")
async def chat_endpoint(history: List[Message]):
    # Convert Pydantic models to simple dicts
    history_dict = [{"role": m.role, "content": m.content} for m in history]
    return chat_engine.query(history_dict)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)