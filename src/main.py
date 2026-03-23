"""CLI-style entrypoint for running the reranking demo scaffold."""

from __future__ import annotations

import argparse
from pathlib import Path

from src import config
from src.pipeline.run_demo import run_demo
from src.utils.logging_utils import setup_logger


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments for the demo runner."""
    parser = argparse.ArgumentParser(description="Run the paper reranking demo scaffold.")
    parser.add_argument(
        "--queries",
        type=Path,
        default=config.DEFAULT_QUERY_FILE,
        help="Path to JSON file containing manually instantiated query schema slots.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=config.DEFAULT_OUTPUT_FILE,
        help="Path to output CSV for reranked results.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=config.TOP_K,
        help="Number of Stage 1 candidates to retrieve per query.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the scaffolded pipeline and print a short summary."""
    args = parse_args()
    logger = setup_logger(__name__)

    logger.info("Starting reranking demo scaffold.")
    logger.info("Queries: %s", args.queries)
    logger.info("Output: %s", args.output)
    logger.info("Top-K: %d", args.top_k)

    # TODO: add argument support for custom weights and embedding model overrides.
    # TODO: add optional debug mode that saves intermediate per-criterion scores.
    results_df = run_demo(query_path=args.queries, output_path=args.output, top_k=args.top_k)

    logger.info("Finished scaffold run. Rows written: %d", len(results_df))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
