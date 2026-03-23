"""Dataclass model for manually instantiated fixed-schema query slots."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class QuerySpec:
    """Manual instantiation of a query under the fixed four-slot schema."""

    raw_query: str
    topic_text: str
    method_text: str
    relationship_text: str
    recency_preference: str
