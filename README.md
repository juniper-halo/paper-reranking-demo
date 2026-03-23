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
mkdir -p .env
cp .env.example .env/.env
```

Set `SEMANTIC_SCHOLAR_API_KEY` in `.env/.env` (or export it directly in your shell).

## Demo Workflow (Notebook-First)

Run the demo using notebooks in this order:

1. `notebooks/01_explore_baseline.ipynb`
  - retrieves baseline candidates from Semantic Scholar
  - saves `data/outputs/notebook_baseline_preview.csv`
2. `notebooks/02_reranking_demo.ipynb`
  - runs two-stage retrieval + reranking
  - saves `data/outputs/notebook_reranked_preview.csv`
  - saves `data/outputs/reranked_results.csv`
3. `notebooks/03_compare_baseline_vs_reranked.ipynb`
  - compares baseline vs reranked outputs side-by-side
  - saves `data/outputs/comparison_rank_shift.csv`
  - saves `data/outputs/comparison_summary.csv`

## Optional CLI Run

If you prefer running from the terminal instead of notebooks:

```bash
python -m src.main \
  --queries data/queries/example_queries.json \
  --top-k 20 \
  --output data/outputs/reranked_results.csv
```

## Current Status

The end-to-end demo flow is implemented:

- Stage 1 retrieval from Semantic Scholar
- Stage 2 semantic + recency scoring with weighted reranking
- Notebook-driven output inspection and comparison artifacts

## Future Work

- dynamic criteria extraction
- LLM-based judging
- larger evaluation set