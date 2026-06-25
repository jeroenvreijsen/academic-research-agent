from __future__ import annotations

import re

from research_agent.models import Paper


class ReferenceValidationError(ValueError):
    pass


def extract_reference_titles(markdown: str) -> list[str]:
    references_section = markdown.split("## References", maxsplit=1)
    if len(references_section) == 1:
        return []

    titles: list[str] = []
    for line in references_section[1].splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        match = re.match(r"-\s+(.+?)(?:\s+\(\d{4}\)|\.|$)", line)
        if match:
            titles.append(match.group(1).strip())
    return titles


def validate_references(markdown: str, retrieved_papers: list[Paper]) -> None:
    # The generated review is checked against retrieved titles so the system does
    # not silently accept invented or unretrieved references.
    retrieved_titles = {_normalize_title(paper.title) for paper in retrieved_papers}
    reference_titles = extract_reference_titles(markdown)

    # A references section is required because the assignment needs evidence that
    # the output is grounded in retrieved academic sources.
    if not reference_titles:
        raise ReferenceValidationError("The literature review has no references.")

    invalid_titles = [
        title
        for title in reference_titles
        if _normalize_title(title) not in retrieved_titles
    ]

    if invalid_titles:
        formatted = ", ".join(invalid_titles)
        raise ReferenceValidationError(
            f"The literature review cites papers that were not retrieved: {formatted}"
        )


def _normalize_title(title: str) -> str:
    return re.sub(r"\s+", " ", title.strip().lower())
