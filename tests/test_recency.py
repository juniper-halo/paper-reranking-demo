"""Tests for recency score normalization."""

from __future__ import annotations

from src.models.paper import Paper
from src.scoring.recency import normalize_recency_scores, score_recency_for_papers


def test_normalize_recency_scores_basic_ordering() -> None:
    years = [2018, 2020, 2022]
    scores = normalize_recency_scores(years)

    assert scores[0] < scores[1] < scores[2]
    assert scores[0] == 0.0
    assert scores[2] == 1.0


def test_normalize_recency_scores_all_equal() -> None:
    years = [2021, 2021, 2021]
    scores = normalize_recency_scores(years)

    assert scores == [1.0, 1.0, 1.0]


def test_score_recency_for_papers_maps_by_id() -> None:
    papers = [
        Paper(paper_id="a", title="Paper A", year=2019),
        Paper(paper_id="b", title="Paper B", year=2021),
    ]

    recency = score_recency_for_papers(papers)

    assert recency["a"] == 0.0
    assert recency["b"] == 1.0
