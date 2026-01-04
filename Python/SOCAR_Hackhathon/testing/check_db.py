from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Initialize the embedding function (same as we used to create it)
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Connect to your existing database
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embedding_function
)

# 3. Count documents
count = db._collection.count()
print(f"\nTotal Documents in DB: {count}")

# 4. Peek at the data (if any exists)
if count > 0:
    print("\n--- First 3 Documents ---")
    results = db.similarity_search("neft", k=3) # Search for "oil" (neft)
    for doc in results:
        print(f"\n[Source: {doc.metadata['source']}, Page: {doc.metadata['page']}]")
        print(f"Content snippet: {doc.page_content[:200]}...")
else:
    print("⚠️ The database is empty! The OCR process found no text.")