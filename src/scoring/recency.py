"""Recency normalization helpers for publication years."""

from __future__ import annotations

from collections.abc import Sequence

from src.models.paper import Paper


def normalize_recency_scores(years: Sequence[int | None]) -> list[float]:
    """Normalize publication years into [0, 1], where newer years score higher.

    Rules:
    - Missing year (`None`) is scored as 0.0 unless all known years are equal.
    - If all known years are equal, all papers receive 1.0 (neutral tie).
    """
    if not years:
        return []

    valid_years = [year for year in years if year is not None]
    if not valid_years:
        return [0.0 for _ in years]

    min_year = min(valid_years)
    max_year = max(valid_years)

    if min_year == max_year:
        return [1.0 for _ in years]

    span = float(max_year - min_year)
    scores: list[float] = []
    for year in years:
        if year is None:
            scores.append(0.0)
        else:
            scores.append((year - min_year) / span)

    return scores


def score_recency_for_papers(papers: Sequence[Paper]) -> dict[str, float]:
    """Compute recency scores keyed by paper id."""
    years = [paper.year for paper in papers]
    normalized = normalize_recency_scores(years)

    return {
        paper.paper_id: score
        for paper, score in zip(papers, normalized, strict=False)
    }
