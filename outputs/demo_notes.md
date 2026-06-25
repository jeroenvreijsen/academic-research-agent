# Demo Notes

## Successful Command-Line Run

The project was demonstrated by running the research agent from the command line with the topic:

```bash
python -m research_agent.main "large language model agents"
```

The run demonstrates that the system can:

- Accept a research topic as a command-line argument.
- Plan a small set of research subgoals for the topic.
- Search OpenAlex for academic papers related to those subgoals.
- Store retrieved papers in a SQLite database.
- Remove duplicate papers before producing the final output.
- Score and filter papers by relevance to the topic.
- Generate a short Markdown literature review using the LLM client abstraction.
- Validate that the final references only cite retrieved papers.
- Save the final review and database in the `outputs/` folder.

The generated `outputs/literature_review.md` contains references only from the current run's retrieved and validated papers.
