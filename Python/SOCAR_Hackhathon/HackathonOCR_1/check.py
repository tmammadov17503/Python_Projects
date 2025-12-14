import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
if not base_url.endswith("/openai/v1/"):
    base_url = base_url.rstrip("/") + "/openai/v1/"

client = OpenAI(
    base_url=base_url,
    api_key=os.getenv("API_KEY"),
)

completion = client.chat.completions.create(
    model=os.getenv("OCR_MODEL_NAME"),
    messages=[
        {
            "role": "user",
            "content": "What is the capital of France?",
        }
    ],
)

print(completion.choices[0].message)
