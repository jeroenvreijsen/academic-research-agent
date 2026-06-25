from __future__ import annotations

import pytest

from research_agent.models import Paper
from research_agent.validator import ReferenceValidationError, validate_references


def test_validate_references_accepts_retrieved_titles() -> None:
    papers = [Paper(openalex_id="1", title="Retrieved Paper", year=2022)]
    markdown = (
        "# Review\n\n"
        "## References\n"
        "- Retrieved Paper (2022). Example Author. https://openalex.org/W1\n"
    )

    validate_references(markdown, papers)


def test_validate_references_rejects_unretrieved_titles() -> None:
    papers = [Paper(openalex_id="1", title="Retrieved Paper", year=2022)]
    markdown = (
        "# Review\n\n"
        "## References\n"
        "- Invented Paper (2024). Example Author. https://example.com\n"
    )

    with pytest.raises(ReferenceValidationError):
        validate_references(markdown, papers)


def test_validate_references_requires_references_section() -> None:
    with pytest.raises(ReferenceValidationError):
        validate_references("# Review\n\nNo references here.\n", [])
