"""Semantic similarity scoring skeletons for schema slots vs paper text."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from src.models.paper import Paper


def cosine_similarity_matrix(query_embeddings: np.ndarray, doc_embeddings: np.ndarray) -> np.ndarray:
    """Compute cosine similarity matrix for query and document embedding matrices.

    TODO: add defensive handling for zero vectors and configurable normalization.
    """
    if query_embeddings.size == 0 or doc_embeddings.size == 0:
        return np.zeros((0, 0), dtype=float)

    query_norm = np.linalg.norm(query_embeddings, axis=1, keepdims=True)
    doc_norm = np.linalg.norm(doc_embeddings, axis=1, keepdims=True)

    query_safe = np.where(query_norm == 0.0, 1.0, query_norm)
    doc_safe = np.where(doc_norm == 0.0, 1.0, doc_norm)

    normalized_q = query_embeddings / query_safe
    normalized_d = doc_embeddings / doc_safe

    return normalized_q @ normalized_d.T


def initialize_zero_semantic_scores(
    papers: Sequence[Paper],
    slot_names: Sequence[str],
) -> dict[str, dict[str, float]]:
    """Create placeholder semantic scores for each paper/slot pair.

    This is intentionally a scaffold helper. It allows pipeline wiring before
    embedding-based similarity is fully implemented.

    TODO: replace this function with true slot-to-paper semantic scoring.
    TODO: add optional score normalization across papers per slot.
    """
    scores: dict[str, dict[str, float]] = {}
    for paper in papers:
        scores[paper.paper_id] = {slot: 0.0 for slot in slot_names}
    return scores
