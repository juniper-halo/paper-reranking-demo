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


def _validate_score_ranges(
    criterion_scores_by_paper: Mapping[str, Mapping[str, float]],
    *,
    min_score: float = 0.0,
    max_score: float = 1.0,
) -> None:
    """Validate per-criterion scores are within the expected normalized range."""
    for paper_id, criterion_scores in criterion_scores_by_paper.items():
        for criterion, score in criterion_scores.items():
            numeric_score = float(score)
            if not (min_score <= numeric_score <= max_score):
                raise ValueError(
                    f"Score out of range for paper '{paper_id}', criterion '{criterion}': "
                    f"{numeric_score} not in [{min_score}, {max_score}]"
                )


def rank_papers(
    papers: Sequence[Paper],
    criterion_scores_by_paper: Mapping[str, Mapping[str, float]],
    weights: Mapping[str, float],
    validate_ranges: bool = True,
) -> list[ScoreResult]:
    """Combine criterion scores and return papers sorted by final score descending."""
    if validate_ranges:
        _validate_score_ranges(criterion_scores_by_paper)

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

    results.sort(
        key=lambda item: (
            item.final_score,
            float(item.criterion_scores.get("recency", 0.0)),
        ),
        reverse=True,
    )

    return results
