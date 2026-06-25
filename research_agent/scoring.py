from __future__ import annotations

import re

from research_agent.models import Paper


STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "for",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}

MIN_RELEVANCE_SCORE = 0.6


def score_paper(paper: Paper, topic: str, subgoal: str = "") -> float:
    topic_words = _tokens(topic)
    subgoal_words = _tokens(subgoal)
    title_words = _tokens(paper.title)
    abstract_words = _tokens(paper.abstract)
    paper_words = title_words | abstract_words

    if not topic_words:
        return 0.0

    topic_overlap = len(topic_words & paper_words) / len(topic_words)
    title_overlap = len(topic_words & title_words) / len(topic_words)
    abstract_overlap = len(topic_words & abstract_words) / len(topic_words)
    subgoal_overlap = 0.0
    if subgoal_words:
        subgoal_overlap = len(subgoal_words & paper_words) / len(subgoal_words)

    score = (
        0.60 * (topic_overlap**3)
        + 0.25 * title_overlap
        + 0.10 * abstract_overlap
        + 0.05 * subgoal_overlap
    )
    return round(min(score, 1.0), 3)


def score_papers(papers: list[Paper], topic: str) -> list[Paper]:
    for paper in papers:
        paper.score = score_paper(paper, topic, paper.subgoal)
    return sorted(papers, key=lambda paper: paper.score, reverse=True)


def filter_relevant_papers(
    papers: list[Paper], minimum_score: float = MIN_RELEVANCE_SCORE
) -> list[Paper]:
    return [paper for paper in papers if paper.score >= minimum_score]


def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-zA-Z0-9-]*", text.lower())
    return {
        _normalize_word(word)
        for word in words
        if word not in STOPWORDS and len(word) > 2
    }


def _normalize_word(word: str) -> str:
    if word.endswith("ies") and len(word) > 4:
        return f"{word[:-3]}y"
    if word.endswith("s") and not word.endswith(("is", "ss")) and len(word) > 4:
        return word[:-1]
    return word
