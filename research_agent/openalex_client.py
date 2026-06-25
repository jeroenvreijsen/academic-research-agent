from __future__ import annotations

from typing import Any

import requests

from research_agent.models import Paper


class OpenAlexClient:
    """Tiny OpenAlex API client.

    OpenAlex does not require an API key. Passing an email address is polite and
    helps OpenAlex contact you if your app causes unusual traffic.
    """

    BASE_URL = "https://api.openalex.org/works"

    def __init__(self, email: str | None = None, timeout: int = 20) -> None:
        self.email = email
        self.timeout = timeout

    def search_papers(self, query: str, limit: int = 5) -> list[Paper]:
        params: dict[str, Any] = {
            "search": query,
            "per-page": limit,
            "sort": "relevance_score:desc",
        }
        if self.email:
            params["mailto"] = self.email

        response = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        return [self._paper_from_work(work) for work in data.get("results", [])]

    def _paper_from_work(self, work: dict[str, Any]) -> Paper:
        authors = [
            authorship.get("author", {}).get("display_name", "")
            for authorship in work.get("authorships", [])
        ]
        authors = [author for author in authors if author]

        doi = work.get("doi") or ""
        if doi.startswith("https://doi.org/"):
            doi = doi.removeprefix("https://doi.org/")

        return Paper(
            openalex_id=work.get("id", ""),
            title=work.get("display_name", "") or "Untitled paper",
            authors=", ".join(authors),
            year=work.get("publication_year"),
            doi=doi,
            abstract=self._abstract_from_inverted_index(
                work.get("abstract_inverted_index")
            ),
            url=work.get("primary_location", {})
            .get("landing_page_url", "")
            or work.get("id", ""),
        )

    def _abstract_from_inverted_index(
        self, inverted_index: dict[str, list[int]] | None
    ) -> str:
        if not inverted_index:
            return ""

        words_by_position: dict[int, str] = {}
        for word, positions in inverted_index.items():
            for position in positions:
                words_by_position[position] = word

        return " ".join(words_by_position[index] for index in sorted(words_by_position))
