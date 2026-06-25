from __future__ import annotations

from research_agent.agent import ResearchAgent
from research_agent.llm_client import LLMClient
from research_agent.models import Paper
from research_agent.store import PaperStore


class FakeOpenAlexClient:
    def search_papers(self, query: str, limit: int = 5) -> list[Paper]:
        return [
            Paper(
                openalex_id=f"https://openalex.org/W{abs(hash(query))}",
                title=f"Study of {query}",
                authors="Ada Lovelace",
                year=2024,
                abstract=f"This paper studies {query}.",
                url="https://example.com/paper",
            )
        ]


class FakeLLMClient(LLMClient):
    def write_literature_review(self, topic: str, papers: list[Paper]) -> str:
        paper = papers[0]
        return (
            f"# Literature Review: {topic}\n\n"
            "## Summary\n"
            "A short summary.\n\n"
            "## References\n"
            f"- {paper.title} ({paper.year}). {paper.authors}. {paper.openalex_id}\n"
        )


class TopicAwareOpenAlexClient:
    def search_papers(self, query: str, limit: int = 5) -> list[Paper]:
        if "first topic" in query:
            return [
                Paper(
                    openalex_id="https://openalex.org/WOLD",
                    title="Old Topic Paper",
                    authors="First Author",
                    year=2020,
                    abstract="This paper belongs to the first topic.",
                )
            ]
        return [
            Paper(
                openalex_id="https://openalex.org/WNEW",
                title="New Topic Paper",
                authors="Second Author",
                year=2024,
                abstract="This paper belongs to the second topic.",
            )
        ]


class AllReferencesLLMClient(LLMClient):
    def write_literature_review(self, topic: str, papers: list[Paper]) -> str:
        lines = [
            f"# Literature Review: {topic}",
            "",
            "## Summary",
            "A short summary.",
            "",
            "## References",
        ]
        for paper in papers:
            lines.append(
                f"- {paper.title} ({paper.year}). {paper.authors}. {paper.openalex_id}"
            )
        return "\n".join(lines) + "\n"


def test_agent_runs_end_to_end(tmp_path) -> None:
    output_dir = tmp_path / "outputs"
    store = PaperStore(tmp_path / "papers.sqlite")
    agent = ResearchAgent(
        openalex_client=FakeOpenAlexClient(),
        llm_client=FakeLLMClient(),
        store=store,
        output_dir=output_dir,
    )

    output_path = agent.run("machine learning in education", papers_per_subgoal=1)

    assert output_path.exists()
    assert output_path.parent == output_dir
    assert "## References" in output_path.read_text(encoding="utf-8")
    assert len(store.get_all_papers()) == 4


def test_agent_clears_old_papers_between_runs(tmp_path) -> None:
    store = PaperStore(tmp_path / "papers.sqlite")
    agent = ResearchAgent(
        openalex_client=TopicAwareOpenAlexClient(),
        llm_client=AllReferencesLLMClient(),
        store=store,
        output_dir=tmp_path,
    )

    agent.run("first topic", papers_per_subgoal=1)
    second_output_path = agent.run("second topic", papers_per_subgoal=1)

    review = second_output_path.read_text(encoding="utf-8")
    stored_titles = {paper.title for paper in store.get_all_papers()}

    assert "New Topic Paper" in review
    assert "Old Topic Paper" not in review
    assert stored_titles == {"New Topic Paper"}


def test_plan_subgoals_returns_three_to_five_items(tmp_path) -> None:
    agent = ResearchAgent(
        openalex_client=FakeOpenAlexClient(),
        llm_client=FakeLLMClient(),
        store=PaperStore(tmp_path / "papers.sqlite"),
        output_dir=tmp_path,
    )

    subgoals = agent.plan_subgoals("AI in science")

    assert 3 <= len(subgoals) <= 5
    assert all("AI in science" in subgoal for subgoal in subgoals)
