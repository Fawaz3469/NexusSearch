"""
clean_movies.py
Cleans the raw movies_metadata.csv: drops corrupted rows, parses genres,
extracts release year, and derives a "copies available" figure from
real vote_count data (more popular movies get more simulated stock).
"""

import pandas as pd
import ast

RAW_MOVIES = "data/movies/movies_metadata.csv"
OUTPUT = "data/movies_clean.csv"

def parse_genres(raw):
    try:
        genre_list = ast.literal_eval(raw)
        names = [g["name"] for g in genre_list if "name" in g]
        return ", ".join(names) if names else "Unknown"
    except (ValueError, SyntaxError):
        return "Unknown"

def main():
    df = pd.read_csv(RAW_MOVIES, low_memory=False)
    total_in = len(df)

    # Drop rows corrupted by shifted columns (a known issue in this dataset)
    df = df[df["adult"].isin(["True", "False"])]

    df["id"] = pd.to_numeric(df["id"], errors="coerce")
    df["vote_average"] = pd.to_numeric(df["vote_average"], errors="coerce")
    df["vote_count"] = pd.to_numeric(df["vote_count"], errors="coerce")

    df = df.dropna(subset=["id", "title", "overview", "vote_average", "vote_count"])
    df = df[df["vote_count"] > 0]

    df["genres"] = df["genres"].apply(parse_genres)
    df["release_year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
    df["copies_available"] = (df["vote_count"] // 50).clip(lower=1, upper=25).astype(int)

    out = df[[
        "id", "title", "genres", "release_year",
        "vote_average", "vote_count", "overview", "copies_available"
    ]].rename(columns={
        "id": "movie_id", "vote_average": "rating", "vote_count": "rating_count"
    })

    out["overview"] = out["overview"].str.slice(0, 400)
    out.to_csv(OUTPUT, index=False)

    print(f"{total_in:,} raw rows -> {len(out):,} cleaned movies with real ratings.")
    print(f"Saved to {OUTPUT}")

if __name__ == "__main__":
    main()
