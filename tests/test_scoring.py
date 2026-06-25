from __future__ import annotations

from research_agent.models import Paper
from research_agent.scoring import filter_relevant_papers, score_paper, score_papers


def test_score_paper_rewards_keyword_overlap() -> None:
    relevant = Paper(
        openalex_id="1",
        title="Neural methods for academic search",
        abstract="Academic search can use neural ranking models.",
        year=2023,
    )
    unrelated = Paper(
        openalex_id="2",
        title="Marine biology observations",
        abstract="This article studies coastal ecosystems.",
        year=2023,
    )

    relevant_score = score_paper(relevant, "neural academic search")
    unrelated_score = score_paper(unrelated, "neural academic search")

    assert relevant_score > unrelated_score


def test_score_papers_sorts_descending() -> None:
    papers = [
        Paper(openalex_id="1", title="Unrelated", abstract="No matching words."),
        Paper(
            openalex_id="2",
            title="Academic search planning",
            abstract="Academic search planning with LLMs.",
        ),
    ]

    scored = score_papers(papers, "academic search planning")

    assert scored[0].openalex_id == "2"
    assert scored[0].score >= scored[1].score


def test_weakly_related_paper_falls_below_threshold() -> None:
    relevant = Paper(
        openalex_id="1",
        title="Large language model agents for academic research workflows",
        abstract="Large language model agents can plan, search, and synthesize research.",
    )
    weak = Paper(
        openalex_id="2",
        title="Large language models for financial sentiment analysis",
        abstract="This paper studies financial sentiment analysis with language models.",
    )

    scored = score_papers([weak, relevant], "large language model agents")
    filtered = filter_relevant_papers(scored)

    assert relevant.score > weak.score
    assert relevant in filtered
    assert weak not in filtered
