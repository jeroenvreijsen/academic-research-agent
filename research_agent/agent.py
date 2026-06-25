from __future__ import annotations

import os
from pathlib import Path

from research_agent.llm_client import LLMClient, TemplateLLMClient
from research_agent.models import Paper
from research_agent.openalex_client import OpenAlexClient
from research_agent.scoring import filter_relevant_papers, score_papers
from research_agent.store import PaperStore
from research_agent.validator import validate_references


class ResearchAgent:
    def __init__(
        self,
        openalex_client: OpenAlexClient | None = None,
        llm_client: LLMClient | None = None,
        store: PaperStore | None = None,
        output_dir: str | Path = "outputs",
    ) -> None:
        self.openalex_client = openalex_client or OpenAlexClient(
            email=os.getenv("OPENALEX_EMAIL")
        )
        self.llm_client = llm_client or TemplateLLMClient()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.store = store or PaperStore(self.output_dir / "papers.sqlite")

    def run(self, topic: str, papers_per_subgoal: int = 5) -> Path:
        # Each run starts with a clean store so papers from previous topics cannot
        # contaminate the current literature review.
        self.store.clear()

        subgoals = self.plan_subgoals(topic)
        papers = self.search_for_papers(subgoals, papers_per_subgoal)
        self.store.add_papers(papers)

        # Deduplication happens before scoring so repeated OpenAlex results do not
        # influence the final paper selection.
        deduped_papers = self.store.remove_duplicates()

        scored_papers = score_papers(deduped_papers, topic)

        # Filtering is applied before generation so the review is based only on
        # papers that meet the minimum relevance threshold.
        relevant_papers = filter_relevant_papers(scored_papers)
        self.store.update_scores(relevant_papers)

        review = self.llm_client.write_literature_review(topic, relevant_papers)

        # Reference validation is kept as a final safety check to reduce the risk
        # of invented or unretrieved references appearing in the output.
        validate_references(review, relevant_papers)

        output_path = self.output_dir / "literature_review.md"
        output_path.write_text(review, encoding="utf-8")
        return output_path

    def plan_subgoals(self, topic: str) -> list[str]:
        return [
            f"Foundational theories and definitions for {topic}",
            f"Recent empirical findings about {topic}",
            f"Common methods and datasets used to study {topic}",
            f"Open challenges and research gaps in {topic}",
        ]

    def search_for_papers(
        self, subgoals: list[str], papers_per_subgoal: int
    ) -> list[Paper]:
        papers: list[Paper] = []
        for subgoal in subgoals:
            results = self.openalex_client.search_papers(
                query=subgoal,
                limit=papers_per_subgoal,
            )
            for paper in results:
                paper.subgoal = subgoal
            papers.extend(results)
        return papers
