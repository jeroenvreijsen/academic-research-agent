from __future__ import annotations

import os
from abc import ABC, abstractmethod

from openai import OpenAI

from research_agent.models import Paper


class LLMClient(ABC):
    @abstractmethod
    def write_literature_review(self, topic: str, papers: list[Paper]) -> str:
        """Return a short Markdown literature review."""


class TemplateLLMClient(LLMClient):
    """Deterministic fallback for testing and demos without an API key.

    Automated tests should not depend on live LLM output because model responses
    can vary. This client keeps the pipeline reproducible while using the same
    interface as the real LLM client.
    """

    def write_literature_review(self, topic: str, papers: list[Paper]) -> str:
        selected_papers = papers[:5]
        if not selected_papers:
            return (
                f"# Literature Review: {topic}\n\n"
                "No papers were retrieved, so a literature review could not be written.\n"
            )

        lines = [
            f"# Literature Review: {topic}",
            "",
            "## Summary",
            (
                f"The retrieved literature on **{topic}** suggests a focused body "
                "of work that can be organized around the most relevant papers "
                "found through OpenAlex."
            ),
            "",
            "## Themes",
        ]

        for paper in selected_papers[:3]:
            year = paper.year or "n.d."
            authors = paper.authors or "Unknown authors"
            lines.append(
                f"- **{paper.title}** ({year}) by {authors} is relevant because "
                f"it matches the research goal `{paper.subgoal}`."
            )

        lines.extend(["", "## Gaps and Next Steps"])
        lines.append(
            "Future work should compare methods, datasets, and evaluation criteria "
            "across these papers before narrowing the research question."
        )

        lines.extend(["", "## References"])
        lines.extend(_reference_lines(selected_papers))

        return "\n".join(lines) + "\n"


class OpenAILLMClient(LLMClient):
    """Real LLM client used when OPENAI_API_KEY is available.

    The LLM is used only for synthesis. Retrieval, scoring, filtering, storage,
    and validation remain deterministic so the agent is easier to test and audit.
    """

    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        self.client = OpenAI()
        self.model = model

    def write_literature_review(self, topic: str, papers: list[Paper]) -> str:
        selected_papers = papers[:5]
        if not selected_papers:
            return TemplateLLMClient().write_literature_review(topic, papers)

        response = self.client.responses.create(
            model=self.model,
            input=self._build_prompt(topic, selected_papers),
        )

        generated_text = response.output_text.strip()

        return (
            f"# Literature Review: {topic}\n\n"
            f"{generated_text}\n\n"
            "## References\n"
            + "\n".join(_reference_lines(selected_papers))
            + "\n"
        )

    def _build_prompt(self, topic: str, papers: list[Paper]) -> str:
        paper_blocks = []
        for index, paper in enumerate(papers, start=1):
            paper_blocks.append(
                "\n".join(
                    [
                        f"Paper {index}",
                        f"Title: {paper.title}",
                        f"Authors: {paper.authors or 'Unknown authors'}",
                        f"Year: {paper.year or 'n.d.'}",
                        f"Subgoal: {paper.subgoal}",
                        f"Abstract: {paper.abstract or 'No abstract available.'}",
                    ]
                )
            )

        return (
            f"Write a concise academic literature review for the topic: {topic}.\n\n"
            "Use only the retrieved papers below. Do not invent studies, authors, "
            "claims, citations, or references.\n\n"
            "Use exactly these Markdown sections:\n"
            "## Summary\n"
            "## Themes\n"
            "## Gaps and Next Steps\n\n"
            "Do not include a title. Do not include a References section, because "
            "the software will add validated references after generation.\n\n"
            "Retrieved papers:\n\n"
            + "\n\n".join(paper_blocks)
        )


def create_llm_client() -> LLMClient:
    if os.getenv("OPENAI_API_KEY"):
        return OpenAILLMClient(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))

    return TemplateLLMClient()


def _reference_lines(papers: list[Paper]) -> list[str]:
    lines = []
    for paper in papers:
        year = paper.year or "n.d."
        authors = paper.authors or "Unknown authors"
        locator = paper.doi or paper.url or paper.openalex_id
        lines.append(f"- {paper.title} ({year}). {authors}. {locator}")
    return lines
