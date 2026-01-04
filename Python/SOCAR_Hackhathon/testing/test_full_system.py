import requests
import json

# 1. Configuration
BASE_URL = "http://127.0.0.1:8000"
PDF_FILE = "Abşeron-Kür MQ Alt Horizontları AYMT və Seysmik-Geofizika_SHORT.pdf"  # Use your actual filename


def run_test():
    print("--- 1. Testing OCR & Ingestion ---")
    try:
        with open(PDF_FILE, "rb") as f:
            files = {"file": f}
            response = requests.post(f"{BASE_URL}/ocr", files=files)

        if response.status_code == 200:
            print("✅ OCR Success! Data saved to Vector DB.")
            # Print a snippet of what was found
            data = response.json()
            if len(data) > 0:
                print(f"   Sample Extracted: {data[0]['MD_text'][:100]}...")
        else:
            print(f"❌ OCR Failed: {response.text}")
            return
    except FileNotFoundError:
        print(f"❌ File {PDF_FILE} not found! Put it in the same folder.")
        return

    print("\n--- 2. Testing Chatbot (RAG) ---")
    # We ask a question that relies on the numbers we just found (965, 134)
    chat_payload = [
        {"role": "user", "content": "What numeric values or depths were found in the seismic maps?"}
    ]

    headers = {"Content-Type": "application/json"}
    chat_response = requests.post(
        f"{BASE_URL}/chat",
        data=json.dumps(chat_payload),
        headers=headers
    )

    if chat_response.status_code == 200:
        result = chat_response.json()
        print("✅ Chatbot Answer:")
        print("------------------------------------------------")
        print(result['answer'])
        print("------------------------------------------------")
        print("Sources Used:")
        for source in result['sources']:
            print(f" - Page {source['page_number']}: {source['content'][:50]}...")
    else:
        print(f"❌ Chatbot Failed: {chat_response.text}")


if __name__ == "__main__":
    run_test()