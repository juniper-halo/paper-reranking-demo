"""Dataclass model for per-paper criterion scores and final ranking score."""

from __future__ import annotations

from dataclasses import dataclass

from src.models.paper import Paper


@dataclass(slots=True)
class ScoreResult:
    """Reranking output for one paper candidate."""

    paper: Paper
    criterion_scores: dict[str, float]
    final_score: float
