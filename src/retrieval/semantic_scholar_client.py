"""Semantic Scholar API client skeleton for candidate retrieval."""

from __future__ import annotations

import json
import time
from typing import Any

import requests
from src.utils.logging_utils import setup_logger

logger = setup_logger(__name__)


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
        fields: str = "paperId,title,abstract,year,authors,venue,url",
    ) -> list[dict[str, Any]]:
        """Search for papers and return raw API records.

        Sends a request to Semantic Scholar's paper search endpoint, applies a
        small retry policy for HTTP 429 responses, and returns the `data` list
        when present.
        """
        headers: dict[str, str] = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key

        params = {
            "query": query.strip(),
            "limit": str(limit),
            "offset": str(offset),
            "fields": str(fields),
        }

        url = f"{self.base_url}/paper/search"
        max_attempts = 3
        response: requests.Response | None = None
        for attempt in range(1, max_attempts + 1):
            response = self.session.get(url, params=params, headers=headers, timeout=15)
            if response.status_code == 429 and attempt < max_attempts:
                retry_after = response.headers.get("Retry-After")
                sleep_seconds = float(retry_after) if retry_after else float(2 ** (attempt - 1))
                logger.warning(
                    "Semantic Scholar 429 rate limit. Retrying in %.1fs (attempt %d/%d).",
                    sleep_seconds,
                    attempt,
                    max_attempts,
                )
                time.sleep(sleep_seconds)
                continue
            break

        if response is None:
            logger.error("No response received from Semantic Scholar API.")
            return []

        response.raise_for_status()

        try:
            payload = response.json()
        except json.decoder.JSONDecodeError as exception:
            logger.exception("Failed to parse Semantic Scholar response as JSON: %s", exception)
            return []

        if not isinstance(payload, dict):
            logger.error("Unexpected response type: %s", type(payload).__name__)
            return []

        data = payload.get("data", [])
        if not isinstance(data, list):
            logger.error("Unexpected 'data' field type: %s", type(data).__name__)
            return []

        return data
