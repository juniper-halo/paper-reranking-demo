"""Semantic similarity scoring helpers for schema slots vs paper text."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from src.models.paper import Paper
from src.models.query_spec import QuerySpec
from src.scoring.embedder import TextEmbedder
from src.utils.text import combine_title_abstract

SEMANTIC_SLOT_NAMES: tuple[str, str, str] = (
    "topic_match",
    "method_match",
    "relationship_match",
)


def cosine_similarity_matrix(query_embeddings: np.ndarray, doc_embeddings: np.ndarray) -> np.ndarray:
    """Compute cosine similarity matrix for query and document embedding matrices."""
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
    """Create placeholder semantic scores for each paper/slot pair."""
    scores: dict[str, dict[str, float]] = {}
    for paper in papers:
        scores[paper.paper_id] = {slot: 0.0 for slot in slot_names}
    return scores


def compute_semantic_scores(
    papers: Sequence[Paper],
    query_spec: QuerySpec,
    embedder: TextEmbedder | None = None,
    slot_names: Sequence[str] = SEMANTIC_SLOT_NAMES,
) -> dict[str, dict[str, float]]:
    """Compute semantic similarity scores for each paper under each requested slot.

    Returns:
    - {paper_id: {slot_name: cosine_similarity}}
    """
    if not papers:
        return {}

    slot_text_by_name: dict[str, str] = {
        "topic_match": query_spec.topic_text,
        "method_match": query_spec.method_text,
        "relationship_match": query_spec.relationship_text,
    }

    selected_slot_texts: list[str] = []
    selected_slot_names: list[str] = []
    for slot_name in slot_names:
        if slot_name not in slot_text_by_name:
            raise ValueError(f"Unsupported semantic slot for similarity scoring: {slot_name}")
        selected_slot_names.append(slot_name)
        selected_slot_texts.append(slot_text_by_name[slot_name])

    local_embedder = embedder or TextEmbedder()
    query_embeddings = local_embedder.encode(selected_slot_texts)

    paper_texts = [combine_title_abstract(paper.title, paper.abstract) for paper in papers]
    paper_embeddings = local_embedder.encode(paper_texts)

    similarity_matrix = cosine_similarity_matrix(query_embeddings, paper_embeddings)

    scores: dict[str, dict[str, float]] = {}
    for paper_idx, paper in enumerate(papers):
        scores[paper.paper_id] = {
            slot_name: float(similarity_matrix[slot_idx, paper_idx])
            for slot_idx, slot_name in enumerate(selected_slot_names)
        }

    return scores
