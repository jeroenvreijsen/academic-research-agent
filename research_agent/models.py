from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Paper:
    """A simple representation of a paper returned by OpenAlex."""

    openalex_id: str
    title: str
    authors: str = ""
    year: int | None = None
    doi: str = ""
    abstract: str = ""
    url: str = ""
    subgoal: str = ""
    score: float = 0.0

    @property
    def citation_key(self) -> str:
        if self.doi:
            return self.doi.lower()
        if self.openalex_id:
            return self.openalex_id.lower()
        return self.title.lower()
