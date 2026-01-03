import pandas as pd

df = pd.read_csv("bbc_news.csv")

def categorize_news(title):
    title = title.lower()

    if any(word in title for word in ["business", "market", "economy", "finance", "stocks", "trade", "money", "invest", "bank", "company", "profit"]):
        return "Business"
    elif any(word in title for word in ["politics", "government", "election", "policy", "minister", "president", "law", "parliament", "vote"]):
        return "Politics"
    elif any(word in title for word in ["sports", "match", "football", "cricket", "tennis", "tournament", "league", "championship", "olympics", "athlete", "game"]):
        return "Sports"
    elif any(word in title for word in ["technology", "tech", "software", "computer", "AI", "cyber", "innovation", "hacking", "internet", "digital"]):
        return "Tech"
    elif any(word in title for word in ["entertainment", "movie", "film", "music", "celebrity", "Hollywood", "Bollywood", "actor", "director", "show", "series"]):
        return "Entertainment"
    elif any(word in title for word in ["health", "medicine", "hospital", "covid", "virus", "vaccine", "doctor", "treatment", "disease", "cancer"]):
        return "Health"
    elif any(word in title for word in ["science", "space", "research", "discovery", "astronomy", "nasa", "experiment", "physics", "biology", "chemistry"]):
        return "Science"
    elif any(word in title for word in ["war", "conflict", "military", "army", "attack", "invasion", "battle", "bomb", "terror", "explosion"]):
        return "World News"
    else:
        return "Other"

df["category"] = df["title"].apply(categorize_news)

print(df[["title", "category"]].head())

df.to_csv("bbc_news_categorized.csv", index=False)

print("Improved categorization.")