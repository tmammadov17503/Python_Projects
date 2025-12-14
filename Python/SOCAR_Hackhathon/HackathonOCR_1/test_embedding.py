import os
from openai import OpenAI

print("Script started")

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY env var is not set")

# IMPORTANT: Using the generic OpenAI client with the full BASE_URL is NOT the standard
# way for Azure embeddings, but we are testing it as a diagnostic step.
BASE_URL = "https://llmapihackathon.services.ai.azure.com/openai/v1/"
MODEL_NAME = "text-embedding-3-large" # This must be the AZURE DEPLOYMENT ID

client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL,
)

print(f"Calling embeddings using generic client at {BASE_URL} for model {MODEL_NAME}...")

try:
    # Note: We are omitting the dimensions parameter for the generic client test 
    # as the complexity of Azure API routing is the goal of this test.
    resp = client.embeddings.create(
        model=MODEL_NAME,
        input=["This is a test sentence to confirm the embedding model works."],
    )

    vec = resp.data[0].embedding
    
    # Cleaned line 25: All spaces are standard
    print("✅ OK:", "dims =", len(vec), "first5 =", vec[:5]) 

except Exception as e:
    print("❌ FAILURE: Embedding API call failed.")
    print(f"Error Details: {e}")


if __name__ == "__main__":
    print("Script finished")