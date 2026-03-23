"""Tests for weighted score aggregation and rank ordering."""

from __future__ import annotations

from src.models.paper import Paper
from src.scoring.weighted_ranker import compute_weighted_score, rank_papers


def test_compute_weighted_score_simple_case() -> None:
    weights = {"topic_match": 0.5, "method_match": 0.5}
    scores = {"topic_match": 0.8, "method_match": 0.6}

    final_score = compute_weighted_score(scores, weights)

    assert abs(final_score - 0.7) < 1e-9


def test_rank_papers_descending_final_score() -> None:
    papers = [
        Paper(paper_id="p1", title="Paper 1"),
        Paper(paper_id="p2", title="Paper 2"),
    ]
    weights = {"topic_match": 1.0}
    criterion_scores = {
        "p1": {"topic_match": 0.2},
        "p2": {"topic_match": 0.9},
    }

    ranked = rank_papers(
        papers=papers,
        criterion_scores_by_paper=criterion_scores,
        weights=weights,
    )

    assert [item.paper.paper_id for item in ranked] == ["p2", "p1"]
    assert ranked[0].final_score == 0.9
