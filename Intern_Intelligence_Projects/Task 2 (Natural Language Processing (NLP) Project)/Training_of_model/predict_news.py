import pickle
import numpy as np

model = pickle.load(open("text_classifier_model.pkl", "rb"))
vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))

def predict_category(text):
    text_tfidf = vectorizer.transform([text])
    prediction = model.predict(text_tfidf)[0]
    return prediction

news_headlines = [
    "Stock markets are crashing due to inflation fears",
    "New AI software revolutionizes healthcare industry",
    "Champions League final ends in dramatic victory",
    "NASA discovers a new exoplanet in distant galaxy"
]

for headline in news_headlines:
    category = predict_category(headline)
    print(f"Headline: {headline}\nPredicted Category: {category}\n")
