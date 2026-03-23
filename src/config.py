"""Project-wide configuration constants for the reranking demo scaffold."""

from __future__ import annotations

import os
from pathlib import Path

# NOTE: Keep this in sync with schema/fixed_schema.py until config is centralized.
DEFAULT_WEIGHTS: dict[str, float] = {
    "topic_match": 0.35,
    "method_match": 0.30,
    "relationship_match": 0.25,
    "recency": 0.10,
}

TOP_K: int = 20
EMBEDDING_MODEL_NAME: str = "sentence-transformers/all-MiniLM-L6-v2"

PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
DATA_DIR: Path = PROJECT_ROOT / "data"
QUERY_DIR: Path = DATA_DIR / "queries"
OUTPUT_DIR: Path = DATA_DIR / "outputs"
CACHE_DIR: Path = DATA_DIR / "cache"

DEFAULT_QUERY_FILE: Path = QUERY_DIR / "example_queries.json"
DEFAULT_OUTPUT_FILE: Path = OUTPUT_DIR / "reranked_results.csv"

SEMANTIC_SCHOLAR_API_KEY: str | None = os.getenv("SEMANTIC_SCHOLAR_API_KEY")