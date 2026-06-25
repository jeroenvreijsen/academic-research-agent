# LLM-Powered Academic Research Planning Agent

## 1. Project Purpose

This project implements a small academic research planning agent. Given a research topic from the command line, the system plans research subgoals, retrieves academic papers from OpenAlex, stores and processes the results, and produces a short Markdown literature review with validated references.

The goal is to demonstrate a clear, testable pipeline for LLM-assisted academic research planning rather than to build a production research platform.

## 2. Implemented Solution Overview

The implemented solution is a simplified single-agent research assistant. It performs the following tasks:

- Accepts a topic from the command line.
- Plans 3 to 5 research subgoals.
- Searches OpenAlex for papers related to each subgoal.
- Stores retrieved papers in SQLite.
- Removes duplicate papers.
- Scores and filters papers by relevance.
- Uses an LLM client abstraction to generate a short Markdown literature review.
- Validates that references in the final review only use retrieved papers.
- Saves outputs to the `outputs/` folder.

The default `TemplateLLMClient` is deterministic and does not require an API key. A real LLM provider can be added later by implementing the `LLMClient` interface.

## 3. Simplification from the Original Proposal

The original proposal involved multiple cooperating agents. For this submission, the design was simplified from multiple cooperating agents into one main ResearchPlanningAgent to reduce coordination complexity and improve reliability while preserving the required planning, retrieval, processing, storage, synthesis, and validation behaviour.

In the code, this single-agent role is implemented by the `ResearchAgent` class in `research_agent/agent.py`.

## 4. Architecture and Workflow

```text
Command line topic
       |
       v
ResearchAgent
       |
       +--> plan subgoals
       |
       +--> search OpenAlex
       |
       +--> store papers in SQLite
       |
       +--> remove duplicates
       |
       +--> score and filter relevance
       |
       +--> generate Markdown review through LLMClient
       |
       +--> validate references
       |
       v
outputs/literature_review.md
outputs/papers.sqlite
```

Main modules:

- `research_agent/main.py`: command-line entry point.
- `research_agent/agent.py`: main research planning workflow.
- `research_agent/openalex_client.py`: OpenAlex search client.
- `research_agent/store.py`: SQLite persistence and deduplication.
- `research_agent/scoring.py`: relevance scoring and filtering.
- `research_agent/llm_client.py`: LLM abstraction and template implementation.
- `research_agent/validator.py`: reference validation.
- `research_agent/models.py`: paper data model.

## 5. Installation Instructions

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Optional: copy `.env.example` to `.env` and set `OPENALEX_EMAIL`. OpenAlex does not require an API key, but an email address is recommended for polite API usage.

## 6. How to Run the Agent

Run the agent with a research topic:

```bash
python -m research_agent.main "large language model agents"
```

Optional argument:

```bash
python -m research_agent.main "large language model agents" --papers-per-subgoal 5
```

Generated outputs:

- `outputs/literature_review.md`
- `outputs/papers.sqlite`

## 7. How to Run Tests

Run the pytest suite:

```bash
pytest
```

If using the project virtual environment directly:

```bash
.venv/bin/python -m pytest
```

## 8. Evidence of Execution

The `outputs/` folder contains evidence files for review:

- `outputs/literature_review.md`: generated Markdown literature review.
- `outputs/papers.sqlite`: SQLite database containing processed papers from the current run.
- `outputs/demo_notes.md`: explanation of what the command-line demo demonstrates.
- `outputs/test_summary.md`: summary of the passing test suite.
- `outputs/remediation_log.md`: development issues found and fixes applied.

The latest verified test run passed 11 tests.

## 9. Testing Strategy

The tests use fake OpenAlex and LLM clients so behavior can be checked without depending on live network responses or external LLM APIs.

The test suite verifies:

- End-to-end agent workflow.
- Subgoal planning.
- SQLite insertion and retrieval.
- Duplicate removal.
- Relevance scoring.
- Relevance threshold filtering.
- Run isolation between topics.
- Reference validation for retrieved and invented papers.

## 10. Key Design Decisions

- A single-agent workflow was chosen to keep the system reliable and easy to understand.
- SQLite was used because it is included with Python and is sufficient for a small academic paper store.
- The store is cleared at the start of each run so papers from previous topics cannot appear in later outputs.
- Deduplication checks DOI first, then OpenAlex ID, then title.
- Relevance scoring favors overlap between the topic/subgoal words and the paper title/abstract.
- The LLM client is abstracted so a real provider can replace the deterministic template later.
- Reference validation checks that the literature review only cites retrieved papers.

## 11. Limitations

- The default literature review generator is template-based, not a real LLM.
- Relevance scoring is keyword-based and does not use embeddings or semantic search.
- OpenAlex results depend on the quality of the search query and available metadata.
- The literature review is intentionally short and should be treated as a planning aid, not a final academic review.
- The project is designed for demonstration and testing, not large-scale paper collection.

## 12. References and Acknowledgements

- OpenAlex is used as the academic paper search source: https://openalex.org/
- Python SQLite support is provided by the standard library `sqlite3` module.
- Testing is implemented with pytest.
- The project structure follows a simple modular Python design to support readability, testability, and university assessment.
