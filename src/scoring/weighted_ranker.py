"""Weighted score aggregation and ranking utilities."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from src.models.paper import Paper
from src.models.score_result import ScoreResult


def compute_weighted_score(
    criterion_scores: Mapping[str, float],
    weights: Mapping[str, float],
) -> float:
    """Compute weighted sum across criteria.

    Missing criterion scores default to 0.0.
    """
    return float(
        sum(
            weights[criterion] * float(criterion_scores.get(criterion, 0.0))
            for criterion in weights
        )
    )


def rank_papers(
    papers: Sequence[Paper],
    criterion_scores_by_paper: Mapping[str, Mapping[str, float]],
    weights: Mapping[str, float],
) -> list[ScoreResult]:
    """Combine criterion scores and return papers sorted by final score descending.

    TODO: add optional tie-breaking strategy (e.g., recency or citation count).
    TODO: add normalization checks to ensure criteria are in consistent ranges.
    """
    results: list[ScoreResult] = []

    for paper in papers:
        scores = dict(criterion_scores_by_paper.get(paper.paper_id, {}))
        final_score = compute_weighted_score(scores, weights)

        results.append(
            ScoreResult(
                paper=paper,
                criterion_scores=scores,
                final_score=final_score,
            )
        )

    results.sort(key=lambda item: item.final_score, reverse=True)
    return results
