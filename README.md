# LLM-Powered Academic Research Planning Agent

## 1. Project Purpose

This project is a small academic research planning agent. The user gives the system a research topic from the command line. The system then breaks the topic into smaller research subgoals, searches for academic papers with OpenAlex, stores and processes the results, and creates a short Markdown literature review with checked references.

The purpose of the project is not to build a full production research tool. The main aim is to show a clear and testable pipeline for an LLM-assisted academic research task.

## 2. Implemented Solution Overview

The final implementation is a single-agent research assistant. I kept the system deliberately small so that the main behaviour could be tested and demonstrated clearly.

The agent can:

* accept a research topic from the command line;
* create research subgoals;
* search OpenAlex for papers related to those subgoals;
* store the retrieved papers in SQLite;
* remove duplicate papers;
* score and filter papers based on relevance;
* use an LLM client to generate a short Markdown literature review;
* validate that the references in the review come from retrieved papers;
* save the output in the `outputs/` folder.

The system includes two LLM client options:

* `OpenAILLMClient`: uses the OpenAI API to generate the final literature review when `OPENAI_API_KEY` is available.
* `TemplateLLMClient`: a deterministic fallback that is used when no OpenAI key is available, and also supports stable testing.

This approach means the system can use a real LLM for the final synthesis step, but it can still run without an API key.

## 3. Simplification from the Original Proposal

The original proposal described a system with multiple cooperating agents. During implementation, I simplified this into one main `ResearchAgent`.

This was a deliberate design choice. A single-agent workflow was easier to test, easier to explain, and more reliable for the assignment scope. The final system still keeps the important behaviours from the proposal: planning, retrieval, processing, storage, synthesis, and validation.

The single-agent role is implemented in:

```text
research_agent/agent.py
```

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

The main files are:

* `research_agent/main.py`: command-line entry point.
* `research_agent/agent.py`: controls the main planning-agent workflow.
* `research_agent/openalex_client.py`: searches OpenAlex for academic papers.
* `research_agent/store.py`: handles SQLite storage and deduplication.
* `research_agent/scoring.py`: scores and filters papers by relevance.
* `research_agent/llm_client.py`: contains the LLM abstraction, OpenAI client, and template fallback.
* `research_agent/validator.py`: checks that final references only use retrieved papers.
* `research_agent/models.py`: defines the paper data model.

## 5. Installation Instructions

Create and activate a virtual environment:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Optional OpenAlex setting:

```bash
export OPENALEX_EMAIL="your_email@example.com"
```

OpenAlex does not require an API key, but adding an email address is recommended for polite API usage.

To use the OpenAI LLM client, set an OpenAI API key before running the agent:

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

Optional model setting:

```bash
export OPENAI_MODEL="gpt-4.1-mini"
```

API keys should never be committed to GitHub.

## 6. How to Run the Agent

Run the agent with a research topic:

```bash
python -m research_agent.main "public service motivation"
```

Optional argument:

```bash
python -m research_agent.main "public service motivation" --papers-per-subgoal 5
```

The generated files are saved here:

* `outputs/literature_review.md`
* `outputs/papers.sqlite`

If `OPENAI_API_KEY` is set, the review body is generated with OpenAI. If no key is available, the system uses the deterministic template client instead.

## 7. How to Run Tests

Run the pytest suite:

```bash
pytest
```

Or run it directly through the virtual environment:

```bash
.venv/bin/python -m pytest
```

## 8. Evidence of Execution

The `outputs/` folder contains evidence that the system has been executed:

* `outputs/literature_review.md`: generated Markdown literature review.
* `outputs/papers.sqlite`: SQLite database with the processed papers from the current run.
* `outputs/demo_notes.md`: short explanation of what the command-line demo shows.
* `outputs/test_summary.md`: summary of the passing test suite.
* `outputs/remediation_log.md`: issues found during development and how they were fixed.

The latest verified test run passed 11 tests.

## 9. Testing Strategy

The automated tests use fake OpenAlex and LLM clients. This avoids depending on live network calls or changing LLM output during testing.

The test suite checks:

* the end-to-end agent workflow;
* subgoal planning;
* SQLite insertion and retrieval;
* duplicate removal;
* relevance scoring;
* relevance threshold filtering;
* run isolation between topics;
* reference validation for retrieved and invented papers.

The real OpenAI client is used for live demonstration, not for unit tests. This is because LLM responses are not fully deterministic, so they are not ideal for repeatable automated tests.

## 10. Key Design Decisions

* I used a single-agent workflow to keep the implementation reliable and understandable.
* SQLite was used because it is lightweight, built into Python, and enough for a small academic paper store.
* The paper store is cleared at the start of each run, so old papers from previous topics cannot appear in a new review.
* Deduplication checks DOI first, then OpenAlex ID, and then title as a fallback.
* Relevance scoring is deterministic because scoring and filtering should be repeatable and testable.
* OpenAI is used for the final literature review synthesis, where natural language generation adds the most value.
* The template LLM client is kept as a fallback so the project can still run without API access.
* Reference validation is used as a safety check, so the final review only cites papers that were actually retrieved.

## 11. Limitations

* The single-agent design is simpler than a full multi-agent system.
* OpenAI usage requires an API key and available API credits.
* If no OpenAI key is set, the system falls back to a template-based review generator.
* The relevance scoring is keyword-based and does not use embeddings or semantic search.
* OpenAlex results depend on the search topic and on the metadata available in OpenAlex.
* The generated literature review is short and should be seen as a research planning aid, not as a final academic literature review.
* The project is designed for demonstration and assessment, not for large-scale academic paper collection.

## 12. References and Acknowledgements

* OpenAlex is used as the academic paper search source: [https://openalex.org/](https://openalex.org/)
* OpenAI is used for optional LLM-based literature review generation.
* Python SQLite support is provided by the standard library `sqlite3` module.
* Testing is implemented with pytest.
* HTTP requests are handled with the `requests` library.
* The OpenAI Python SDK is used for the OpenAI LLM client.
* The project structure follows a simple modular Python design to support readability, testing, and demonstration.
