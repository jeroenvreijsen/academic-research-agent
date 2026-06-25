from __future__ import annotations

from research_agent.models import Paper
from research_agent.store import PaperStore


def test_store_adds_and_reads_papers(tmp_path) -> None:
    store = PaperStore(tmp_path / "papers.sqlite")
    paper = Paper(
        openalex_id="https://openalex.org/W1",
        title="A Useful Paper",
        authors="Grace Hopper",
        year=2020,
        doi="10.123/example",
    )

    store.add_papers([paper])

    papers = store.get_all_papers()
    assert len(papers) == 1
    assert papers[0].title == "A Useful Paper"
    assert papers[0].doi == "10.123/example"


def test_remove_duplicates_prefers_highest_score(tmp_path) -> None:
    store = PaperStore(tmp_path / "papers.sqlite")
    low_score = Paper(
        openalex_id="https://openalex.org/W1",
        title="Duplicate Paper",
        doi="10.123/duplicate",
        score=0.2,
    )
    high_score = Paper(
        openalex_id="https://openalex.org/W2",
        title="Duplicate Paper",
        doi="10.123/duplicate",
        score=0.8,
    )
    store.add_papers([low_score, high_score])

    papers = store.remove_duplicates()

    assert len(papers) == 1
    assert papers[0].score == 0.8
