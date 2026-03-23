"""Text preprocessing helpers for scoring inputs."""

from __future__ import annotations


def combine_title_abstract(title: str, abstract: str | None) -> str:
    """Combine title and abstract into one scoring text field."""
    clean_title = title.strip()
    clean_abstract = (abstract or "").strip()

    if clean_abstract:
        return f"{clean_title}\n\n{clean_abstract}".strip()
    return clean_title
