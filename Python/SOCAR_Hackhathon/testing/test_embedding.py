import os
from openai import OpenAI

print("Script started")

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY env var is not set")

BASE_URL = "https://llmapihackathon.services.ai.azure.com/openai/v1/"

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

print("Calling embeddings...")

resp = client.embeddings.create(
    model="text-embedding-3-large",
    input=["This is a test sentence to confirm the embedding model works."],
)

vec = resp.data[0].embedding
print("✅ OK:", "dims =", len(vec), "first5 =", vec[:5])
