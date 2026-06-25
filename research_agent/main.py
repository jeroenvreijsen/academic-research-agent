from __future__ import annotations

import argparse

from research_agent.agent import ResearchAgent


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan an academic research topic and write a short literature review."
    )
    parser.add_argument("topic", help="Research topic to investigate")
    parser.add_argument(
        "--papers-per-subgoal",
        type=int,
        default=5,
        help="Number of OpenAlex results to fetch for each subgoal",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Folder where the SQLite database and Markdown review will be saved",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    agent = ResearchAgent(output_dir=args.output_dir)
    output_path = agent.run(
        topic=args.topic,
        papers_per_subgoal=args.papers_per_subgoal,
    )
    print(f"Saved literature review to {output_path}")


if __name__ == "__main__":
    main()
