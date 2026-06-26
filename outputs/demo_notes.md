# Demo Notes

## Successful Command-Line Run

The project was demonstrated by running the research agent from the command line with the topic:

```bash
python -m research_agent.main "public service motivation"
```

This was used as the final API-backed demo topic because it produced a clear literature review with relevant academic references.

The run demonstrates that the system can:

* Accept a research topic as a command-line argument.
* Plan a small set of research subgoals for the topic.
* Search OpenAlex for academic papers related to those subgoals.
* Store retrieved papers in a SQLite database.
* Remove duplicate papers before producing the final output.
* Score and filter papers by relevance to the topic.
* Generate a short Markdown literature review through the LLM client.
* Use OpenAI for the review body when `OPENAI_API_KEY` is available.
* Fall back to the deterministic template client when no OpenAI API key is available.
* Validate that the final references only cite retrieved papers.
* Save the final review and database in the `outputs/` folder.

The generated `outputs/literature_review.md` contains references only from the current run's retrieved and validated papers.
