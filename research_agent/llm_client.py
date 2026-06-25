from __future__ import annotations

from abc import ABC, abstractmethod

from research_agent.models import Paper


class LLMClient(ABC):
    @abstractmethod
    def write_literature_review(self, topic: str, papers: list[Paper]) -> str:
        """Return a short Markdown literature review."""


class TemplateLLMClient(LLMClient):
    """Deterministic stand-in for a real LLM provider.

    The rest of the agent depends on this small interface, so replacing it with
    an OpenAI, Anthropic, or local-model client only requires implementing one
    method.
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
        for paper in selected_papers:
            year = paper.year or "n.d."
            authors = paper.authors or "Unknown authors"
            locator = paper.doi or paper.url or paper.openalex_id
            lines.append(f"- {paper.title} ({year}). {authors}. {locator}")

        return "\n".join(lines) + "\n"
