import os
import requests
from dotenv import load_dotenv

# === Load .env ===
load_dotenv()
API_KEY = os.getenv("API_KEY")

# === Azure endpoint ===
BASE_URL = "https://llmapihackathon.services.ai.azure.com/openai/v1/"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

response = requests.get(f"{BASE_URL}models", headers=headers)

if response.status_code == 200:
    data = response.json()
    print("✅ Available models:")
    for model in data.get("data", []):
        print("-", model.get("id"))
else:
    print("❌ Error:", response.status_code, response.text)
