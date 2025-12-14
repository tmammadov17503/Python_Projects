import os
import requests
from dotenv import load_dotenv

# === Load .env ===
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://llmapihackathon.services.ai.azure.com/openai/v1/")

headers = {
    "api-key": API_KEY,
    "Content-Type": "application/json"
}

# 1️⃣ Get list of all available model names from /models
print("🔍 Fetching available model names...")
response = requests.get(f"{BASE_URL}models", headers={"Authorization": f"Bearer {API_KEY}"})
if response.status_code != 200:
    print("❌ Could not list models:", response.status_code, response.text)
    exit()

models = [m["id"] for m in response.json().get("data", [])]
print(f"Found {len(models)} model IDs.")

# 2️⃣ Try each as a deployment name using /embeddings endpoint (fast & safe)
print("\n🔎 Testing which models are actually deployed (as valid deployment names)...\n")

valid_deployments = []
for model_name in models:
    try:
        test_payload = {"input": "Test embedding ping", "model": model_name}
        r = requests.post(f"{BASE_URL}embeddings", headers=headers, json=test_payload)

        if r.status_code == 200:
            print(f"✅ ACTIVE DEPLOYMENT: {model_name}")
            valid_deployments.append(model_name)
        elif r.status_code == 404:
            print(f"❌ {model_name} — not deployed (404 Resource not found)")
        elif r.status_code == 400:
            if "Unknown model" in r.text:
                print(f"❌ {model_name} — unknown model name (400 Unknown model)")
            else:
                print(f"⚠️  {model_name} — 400 Bad Request, possible non-embedding model")
        else:
            print(f"⚠️  {model_name} — Unexpected {r.status_code}: {r.text[:80]}")

    except Exception as e:
        print(f"⚠️  {model_name} — Error: {e}")

# 3️⃣ Print summary
print("\n=== SUMMARY ===")
if valid_deployments:
    print("✅ Valid deployment names you can actually call:")
    for d in valid_deployments:
        print("   •", d)
else:
    print("❌ No valid deployments detected via embedding endpoint.")
