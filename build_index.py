"""
build_index.py
Builds the 'products' ChromaDB collection from the full cleaned dataset,
processed in batches to keep memory low. Text gets embedded automatically
using ChromaDB's default local model.
"""

import pandas as pd
import chromadb

BATCH_SIZE = 1000

def main():
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("products")

    reader = pd.read_csv("data/products_clean.csv", chunksize=BATCH_SIZE)
    total = 0
    for chunk in reader:
        ids = chunk["asin"].astype(str).tolist()
        documents = (chunk["title"] + " — " + chunk["category_name"]).tolist()
        metadatas = chunk[["title", "category_name", "stars", "reviews", "price", "isBestSeller"]].to_dict("records")
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
        total += len(chunk)
        print(f"  Indexed {total:,} / 1,383,557 products...")

    print(f"\nDone. Products collection ready with {total:,} items.")

if __name__ == "__main__":
    main()
