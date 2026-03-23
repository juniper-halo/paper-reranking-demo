"""Definitions for the fixed four-slot reranking schema."""

from __future__ import annotations

FIXED_SCHEMA_SLOTS: tuple[str, str, str, str] = (
    "topic_match",
    "method_match",
    "relationship_match",
    "recency",
)

# topic_match: how closely a paper aligns with the topic/subdomain of interest.
# method_match: how well paper methods align with requested methodological cues.
# relationship_match: whether the paper captures the desired variable/concept relationship.
# recency: publication-year freshness normalized to [0, 1].
DEFAULT_SCHEMA_WEIGHTS: dict[str, float] = {
    "topic_match": 0.35,
    "method_match": 0.30,
    "relationship_match": 0.25,
    "recency": 0.10,
}

# TODO: add schema validation helper to enforce key set and weight sum.
