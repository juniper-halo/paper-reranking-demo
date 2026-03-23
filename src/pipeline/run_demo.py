"""Orchestration skeleton for the two-stage retrieval and reranking demo."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src import config
from src.models.score_result import ScoreResult
from src.retrieval.candidate_retriever import CandidateRetriever
from src.retrieval.semantic_scholar_client import SemanticScholarClient
from src.schema.query_instantiator import load_query_specs
from src.scoring.recency import score_recency_for_papers
from src.scoring.semantic_similarity import initialize_zero_semantic_scores
from src.scoring.weighted_ranker import rank_papers
from src.utils.logging_utils import setup_logger


def _results_to_rows(raw_query: str, ranked: list[ScoreResult]) -> list[dict[str, object]]:
    """Convert score dataclasses into tabular rows for CSV export."""
    rows: list[dict[str, object]] = []
    for item in ranked:
        row: dict[str, object] = {
            "raw_query": raw_query,
            "paper_id": item.paper.paper_id,
            "title": item.paper.title,
            "year": item.paper.year,
            "final_score": item.final_score,
        }
        row.update(item.criterion_scores)
        rows.append(row)
    return rows


def run_demo(
    query_path: Path | str = config.DEFAULT_QUERY_FILE,
    output_path: Path | str = config.DEFAULT_OUTPUT_FILE,
    top_k: int = config.TOP_K,
) -> pd.DataFrame:
    """Run the scaffold pipeline and return a dataframe of ranked results.

    This function intentionally contains TODO-heavy placeholders. It establishes
    the expected control flow and interfaces for later implementation.
    """
    logger = setup_logger(__name__)

    # 1) Load query specs.
    query_specs = load_query_specs(query_path)

    # 2) Retrieve candidate papers.
    client = SemanticScholarClient(api_key=config.SEMANTIC_SCHOLAR_API_KEY)
    retriever = CandidateRetriever(client=client)

    all_rows: list[dict[str, object]] = []

    for query_spec in query_specs:
        logger.info("Running query: %s", query_spec.raw_query)

        candidates = retriever.retrieve_candidates(raw_query=query_spec.raw_query, top_k=top_k)

        if not candidates:
            logger.warning(
                "No candidates retrieved for query. TODO: implement Semantic Scholar API retrieval details."
            )
            continue

        # 3) Compute semantic criterion scores.
        # TODO: replace zero placeholder with embedding-based similarity scoring.
        semantic_scores = initialize_zero_semantic_scores(
            papers=candidates,
            slot_names=("topic_match", "method_match", "relationship_match"),
        )

        # 4) Compute normalized recency score.
        recency_scores = score_recency_for_papers(candidates)

        # 5) Combine scores with weighted sum and rerank.
        criterion_scores_by_paper: dict[str, dict[str, float]] = {}
        for paper in candidates:
            per_paper_scores = dict(semantic_scores.get(paper.paper_id, {}))
            per_paper_scores["recency"] = recency_scores.get(paper.paper_id, 0.0)
            criterion_scores_by_paper[paper.paper_id] = per_paper_scores

        ranked = rank_papers(
            papers=candidates,
            criterion_scores_by_paper=criterion_scores_by_paper,
            weights=config.DEFAULT_WEIGHTS,
        )

        # 6) Save outputs (batched across queries; write once at end).
        all_rows.extend(_results_to_rows(raw_query=query_spec.raw_query, ranked=ranked))

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results_df = pd.DataFrame(all_rows)
    results_df.to_csv(output_path, index=False)

    logger.info("Saved results to %s", output_path)
    return results_df
