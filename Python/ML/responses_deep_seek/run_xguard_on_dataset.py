import json
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1) Load X-Guard
model_id = "saillab/x-guard"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(model_id)

# 2) Load your dataset
with open("responses_deepseek_r1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 3) Process each response
results = []
labels = model.config.id2label  # maps numeric outputs to label names

for item in data:
    text = item["response"]

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)

    pred_id = outputs.logits.argmax(dim=-1).item()
    pred_label = labels[pred_id]

    results.append({
        "id": item.get("id"),
        "response": text,
        "prediction": pred_label
    })

# 4) Save results to CSV
df = pd.DataFrame(results)
df.to_csv("x_guard_results.csv", index=False, encoding="utf-8")

print("✅ Classification complete! Saved to x_guard_results.csv")