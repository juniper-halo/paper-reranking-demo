# Q3 Scholarly Paper Reranking Demo

A simplified, reproducible Python demo for second-stage scholarly paper reranking.

This project is intentionally not a full Asta reimplementation. The focus is a clear baseline scaffold for:

1. Stage 1 retrieval: get top-K candidate papers from Semantic Scholar.
2. Stage 2 reranking: score candidates with a fixed relevance schema and sort by final weighted score.

## Fixed Relevance Schema (4 Slots)

The reranker uses a fixed schema with four criteria:

- `topic_match`
- `method_match`
- `relationship_match`
- `recency`

Default weights:

- `topic_match`: 0.35
- `method_match`: 0.30
- `relationship_match`: 0.25
- `recency`: 0.10

For each query, schema slot values are manually instantiated and stored in `data/queries/example_queries.json`.

## Pipeline Overview

1. Load manually instantiated query specs.
2. Retrieve top-K candidates from Semantic Scholar.
3. Compute semantic similarity between each slot text and paper title+abstract.
4. Compute normalized recency score.
5. Combine with weighted sum.
6. Rerank descending by final score.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set `SEMANTIC_SCHOLAR_API_KEY` in your environment (or `.env`, if you use a dotenv loader).

Run the scaffolded demo pipeline:

```bash
python -m src.main \
  --queries data/queries/example_queries.json \
  --top-k 20 \
  --output data/outputs/reranked_results.csv
```

## Current Status

This repository currently provides a modular scaffold with TODO-marked placeholders:

- retrieval client and candidate conversion are skeletonized
- semantic embedding/similarity logic is scaffolded
- recency normalization and weighted combination are lightly implemented

## TODO: Future Work

- dynamic criteria extraction
- LLM-based judging
- larger evaluation set

## Security Note

A previous local file (`test.py`) contained a raw API key string and has been removed from this scaffold. Rotate/revoke that key immediately if it was ever used.
