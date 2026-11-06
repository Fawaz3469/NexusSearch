"""
test_search.py
Quick sanity check: run a few natural-language queries against
both collections and print the top matches with distance scores.
"""

import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
products = client.get_collection("products")
movies = client.get_collection("movies")

def show(title, results, fields):
    print(f"\n=== {title} ===")
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]
    for doc, meta, dist in zip(docs, metas, dists):
        line = " | ".join(f"{f}: {meta.get(f)}" for f in fields)
        print(f"  (distance {dist:.3f}) {line}")

product_queries = ["wireless phone charger", "kitchen knife set", "yoga mat"]
for q in product_queries:
    res = products.query(query_texts=[q], n_results=5)
    show(f"PRODUCTS: '{q}'", res, ["title", "category_name", "stars", "price"])

movie_queries = ["superhero team fighting aliens", "romantic comedy", "space adventure"]
for q in movie_queries:
    res = movies.query(query_texts=[q], n_results=5)
    show(f"MOVIES: '{q}'", res, ["title", "genres", "rating", "release_year"])
