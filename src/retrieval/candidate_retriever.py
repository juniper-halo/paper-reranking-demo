"""Candidate retriever wrapper that converts raw API records to Paper objects."""

from __future__ import annotations

from typing import Any

from src.models.paper import Paper
from src.retrieval.semantic_scholar_client import SemanticScholarClient


class CandidateRetriever:
    """Facade for Stage 1 retrieval from Semantic Scholar."""

    def __init__(self, client: SemanticScholarClient) -> None:
        """Store the API client dependency."""
        self.client = client

    def retrieve_candidates(self, raw_query: str, top_k: int) -> list[Paper]:
        """Retrieve and convert candidate papers for a raw query.

        TODO: refine conversion with robust field validation and error handling.
        """
        raw_records = self.client.search_papers(query=raw_query, limit=top_k)
        papers: list[Paper] = []

        for record in raw_records:
            papers.append(self._record_to_paper(record))

        return papers

    def _record_to_paper(self, record: dict[str, Any]) -> Paper:
        """Convert one raw Semantic Scholar record to a Paper dataclass.

        TODO: map additional metadata fields (authors, venue, citation counts, etc.).
        """
        authors_raw = record.get("authors") or []
        authors: list[str] = [a.get("name", "") for a in authors_raw if isinstance(a, dict)]

        return Paper(
            paper_id=str(record.get("paperId") or record.get("externalIds", {}).get("CorpusId", "")),
            title=str(record.get("title", "")),
            abstract=record.get("abstract"),
            year=record.get("year"),
            venue=record.get("venue"),
            url=record.get("url"),
            authors=authors,
            raw=record,
        )
