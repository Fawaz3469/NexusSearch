"""
clean_products.py
Cleans the raw Amazon products CSV in batches (keeps memory usage low),
merges in category names, and removes duplicate/near-duplicate listings.
"""

import pandas as pd
import re

RAW_PRODUCTS = "data/products/amazon_products.csv"
RAW_CATEGORIES = "data/products/amazon_categories.csv"
OUTPUT = "data/products_clean.csv"
CHUNK_SIZE = 50_000

def normalize_title(title: str) -> str:
    """Lowercase + strip punctuation/extra spaces so near-duplicate titles collapse together."""
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title

def main():
    categories = pd.read_csv(RAW_CATEGORIES)
    cat_map = dict(zip(categories["id"], categories["category_name"]))

    seen_titles = set()
    first_chunk = True
    total_in = 0
    total_out = 0

    reader = pd.read_csv(RAW_PRODUCTS, chunksize=CHUNK_SIZE)
    for chunk in reader:
        total_in += len(chunk)

        chunk = chunk.dropna(subset=["title"])
        chunk = chunk[chunk["title"].str.strip() != ""]

        chunk = chunk.copy()
        chunk["norm_title"] = chunk["title"].apply(normalize_title)
        chunk = chunk[~chunk["norm_title"].isin(seen_titles)]
        chunk = chunk.drop_duplicates(subset="norm_title")
        seen_titles.update(chunk["norm_title"].tolist())

        chunk["category_name"] = chunk["category_id"].map(cat_map).fillna("Uncategorized")
        chunk["stars"] = pd.to_numeric(chunk["stars"], errors="coerce").fillna(0.0)
        chunk["price"] = pd.to_numeric(chunk["price"], errors="coerce").fillna(0.0)
        chunk["reviews"] = pd.to_numeric(chunk["reviews"], errors="coerce").fillna(0).astype(int)

        out = chunk[["asin", "title", "category_name", "stars", "reviews", "price", "isBestSeller"]]
        out.to_csv(OUTPUT, mode="w" if first_chunk else "a", header=first_chunk, index=False)
        first_chunk = False
        total_out += len(out)
        print(f"Processed {total_in:,} rows so far -> kept {total_out:,} unique products")

    print(f"\nDone. {total_in:,} raw rows -> {total_out:,} cleaned, deduplicated products.")
    print(f"Removed {total_in - total_out:,} duplicates/invalid rows.")
    print(f"Saved to {OUTPUT}")

if __name__ == "__main__":
    main()
