# NexusSearch

NexusSearch is a Python project for preparing product and movie datasets and experimenting with semantic search using [ChromaDB](https://www.trychroma.com/).

The repository currently contains data-cleaning scripts, a product-indexing script, and a small search sanity-check script. The documentation below describes the code currently present in the repository; it does not assume that unimplemented application features are available.

## Project status

**Current implementation**

- Cleans movie metadata from `data/movies/movies_metadata.csv` into `data/movies_clean.csv`.
- Cleans product data in batches, joins category names, and removes duplicate product titles.
- Builds a persistent ChromaDB collection named `products` from `data/products_clean.csv`.
- Includes a search test script that queries both `products` and `movies` collections.

**Known setup gaps to resolve**

The scripts reference input/output files that were not present in the repository snapshot used to prepare this README:

- `clean_products.py` expects `data/products/amazon_products.csv`.
- `clean_products.py` writes `data/products_clean.csv`.
- `build_index.py` reads `data/products_clean.csv`.
- `test_search.py` expects both `products` and `movies` ChromaDB collections, but the supplied `build_index.py` only creates/populates `products`.

Consequently, a fresh clone cannot complete the full product pipeline or run the complete search test until the missing product source data is supplied and a movie-indexing step is implemented or the expected `movies` collection is otherwise created.

## Repository structure

```text
NexusSearch/
├── build_index.py
├── clean_movies.py
├── clean_products.py
├── test_search.py
├── requirements.txt
├── .gitignore
└── data/
    ├── movies/
    │   ├── keywords.csv
    │   ├── links.csv
    │   ├── links_small.csv
    │   ├── movies_metadata.csv
    │   └── ratings_small.csv
    ├── products/
    │   └── amazon_categories.csv
    └── movies_clean.csv
```

Generated files and local environments are intentionally excluded from Git:

- `.venv/` and `venv/`
- `chroma_db/`
- Python cache files and local OS/IDE files

## Requirements

- Python 3.10 or newer is recommended.
- pip
- The Python packages listed in `requirements.txt`

The current scripts use pandas for CSV processing and ChromaDB for persistent vector storage and semantic queries.

## Installation

Clone the repository:

```bash
git clone https://github.com/Fawaz3469/NexusSearch.git
cd NexusSearch
```

Create and activate a virtual environment.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows PowerShell**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Data preparation

### Clean movie metadata

The movie-cleaning script reads:

```text
data/movies/movies_metadata.csv
```

Run:

```bash
python clean_movies.py
```

It writes:

```text
data/movies_clean.csv
```

The script parses genre metadata, converts numeric fields, removes invalid rows, derives a release year, and calculates a `copies_available` value from `vote_count`. That availability value is a derived/simulated field, not verified real-world inventory.

### Clean product data

The product-cleaning script expects both of these files:

```text
data/products/amazon_products.csv
data/products/amazon_categories.csv
```

The categories CSV is present in this repository. The products CSV was not included in the repository snapshot and must be obtained separately from a source you are permitted to use.

Once the expected products CSV is available, run:

```bash
python clean_products.py
```

The script writes:

```text
data/products_clean.csv
```

It processes the source in chunks, removes blank titles and duplicate/near-duplicate normalized titles, maps category IDs to category names, and converts selected numeric fields.

## Build the product vector index

After `data/products_clean.csv` has been generated, run:

```bash
python build_index.py
```

The script creates or opens a persistent ChromaDB database at:

```text
./chroma_db
```

It creates/uses a collection named `products`, reads the cleaned product CSV in batches of 1,000, and adds product IDs, text documents, and metadata. ChromaDB's default embedding function is used by the current script.

The first indexing run may take time and may download the embedding model required by ChromaDB. The resulting database is local and is excluded from Git because it is generated data.

## Search sanity check

Run:

```bash
python test_search.py
```

The script issues example natural-language queries against:

- `products`
- `movies`

It prints the top matches and distance values. **At present, the checked-in `build_index.py` only builds the `products` collection.** A `movies` collection must be created separately before the movie queries in `test_search.py` can run successfully.

## Rebuilding the local database

The ChromaDB directory is not committed. To recreate the product index on another machine:

1. Install the dependencies.
2. Obtain the required product source CSV.
3. Run `python clean_products.py`.
4. Run `python build_index.py`.

This recreates the `products` collection from the cleaned product data. The current repository does not yet include a corresponding movie-index-building script.

## Data and licensing

The repository includes CSV datasets. Before redistributing this repository publicly or using the datasets in a commercial project, verify the original source, licence, attribution requirements, and redistribution permissions for each dataset. The presence of a dataset in this repository does not itself establish permission to redistribute it.

## Development notes

- Keep virtual environments, secrets, and generated vector databases out of Git.
- Do not commit API keys, credentials, or private `.env` files.
- If new runtime packages are introduced, update `requirements.txt`.
- If the movie collection is implemented, document its data source and indexing procedure here.

## License

No project licence has been specified yet. Until a licence is added, do not assume that others have permission to reuse, modify, or redistribute this project's code. Add a `LICENSE` file once you have chosen the intended licence.
