"""Dataclass model for paper metadata used in retrieval and reranking."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Paper:
    """A scholarly paper candidate and selected metadata fields."""

    paper_id: str
    title: str
    abstract: str | None = None
    year: int | None = None
    venue: str | None = None
    url: str | None = None
    authors: list[str] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)
