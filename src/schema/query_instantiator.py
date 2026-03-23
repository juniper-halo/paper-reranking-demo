"""Load manually instantiated query schema values from JSON files."""

from __future__ import annotations

from pathlib import Path

from src.models.query_spec import QuerySpec
from src.utils.io import load_json


def load_query_specs(path: Path | str) -> list[QuerySpec]:
    """Load query specs from disk into QuerySpec dataclasses.

    Expected shape:
    {
      "queries": [
        {
          "raw_query": "...",
          "topic_text": "...",
          "method_text": "...",
          "relationship_text": "...",
          "recency_preference": "recent"
        }
      ]
    }
    """
    payload = load_json(path)
    query_items = payload.get("queries", [])

    specs: list[QuerySpec] = []
    for item in query_items:
        specs.append(
            QuerySpec(
                raw_query=str(item.get("raw_query", "")),
                topic_text=str(item.get("topic_text", "")),
                method_text=str(item.get("method_text", "")),
                relationship_text=str(item.get("relationship_text", "")),
                recency_preference=str(item.get("recency_preference", "recent")),
            )
        )

    return specs
