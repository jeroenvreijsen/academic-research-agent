from __future__ import annotations

import sqlite3
from pathlib import Path

from research_agent.models import Paper


class PaperStore:
    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.create_tables()

    def connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_tables(self) -> None:
        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    openalex_id TEXT,
                    title TEXT NOT NULL,
                    authors TEXT,
                    year INTEGER,
                    doi TEXT,
                    abstract TEXT,
                    url TEXT,
                    subgoal TEXT,
                    score REAL DEFAULT 0
                )
                """
            )

    def add_papers(self, papers: list[Paper]) -> None:
        with self.connect() as connection:
            connection.executemany(
                """
                INSERT INTO papers (
                    openalex_id, title, authors, year, doi, abstract, url, subgoal, score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        paper.openalex_id,
                        paper.title,
                        paper.authors,
                        paper.year,
                        paper.doi,
                        paper.abstract,
                        paper.url,
                        paper.subgoal,
                        paper.score,
                    )
                    for paper in papers
                ],
            )

    def get_all_papers(self) -> list[Paper]:
        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT openalex_id, title, authors, year, doi, abstract, url, subgoal, score
                FROM papers
                ORDER BY score DESC, year DESC, title ASC
                """
            ).fetchall()
        return [self._paper_from_row(row) for row in rows]

    def replace_all_papers(self, papers: list[Paper]) -> None:
        with self.connect() as connection:
            connection.execute("DELETE FROM papers")
        self.add_papers(papers)

    def clear(self) -> None:
        with self.connect() as connection:
            connection.execute("DELETE FROM papers")

    def remove_duplicates(self) -> list[Paper]:
        papers = self.get_all_papers()
        unique_papers: dict[str, Paper] = {}

        for paper in papers:
            key = self._dedupe_key(paper)
            existing = unique_papers.get(key)
            if existing is None or paper.score > existing.score:
                unique_papers[key] = paper

        deduped = list(unique_papers.values())
        self.replace_all_papers(deduped)
        return deduped

    def update_scores(self, papers: list[Paper]) -> None:
        self.replace_all_papers(papers)

    def _dedupe_key(self, paper: Paper) -> str:
        if paper.doi:
            return f"doi:{paper.doi.lower()}"
        if paper.openalex_id:
            return f"openalex:{paper.openalex_id.lower()}"
        return f"title:{paper.title.strip().lower()}"

    def _paper_from_row(self, row: sqlite3.Row) -> Paper:
        return Paper(
            openalex_id=row["openalex_id"] or "",
            title=row["title"],
            authors=row["authors"] or "",
            year=row["year"],
            doi=row["doi"] or "",
            abstract=row["abstract"] or "",
            url=row["url"] or "",
            subgoal=row["subgoal"] or "",
            score=float(row["score"] or 0),
        )
