"""Semantic Scholar API client skeleton for candidate retrieval."""

from __future__ import annotations

from typing import Any, Sequence

import requests


class SemanticScholarClient:
    """Minimal wrapper around Semantic Scholar Graph API endpoints."""

    base_url: str = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: str | None = None, session: requests.Session | None = None) -> None:
        """Initialize a client with optional API key and requests session."""
        self.api_key = api_key
        self.session = session or requests.Session()

    def search_papers(
        self,
        query: str,
        limit: int = 20,
        offset: int = 0,
        fields: Sequence[str] | None = None,
    ) -> list[dict[str, Any]]:
        """Search for papers and return raw API records.

        TODO: implement live API call with retries, timeout handling, and pagination.
        TODO: support field selection and request parameter validation.
        TODO: parse and return stable normalized response shape.
        """
        _ = query, limit, offset, fields
        return []
