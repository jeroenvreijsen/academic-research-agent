# Test Summary

The pytest suite contains 11 passing tests. Together, they verify the main behavior required for the academic research planning agent.

## Verified Areas

- Agent flow: confirms the agent can plan subgoals, retrieve papers through a mock OpenAlex client, store results, generate a Markdown review, and save it to the output folder.
- Subgoal planning: confirms the agent creates between 3 and 5 subgoals and keeps them connected to the input topic.
- SQLite storage: confirms papers can be inserted into and read back from the SQLite database.
- Deduplication: confirms duplicate papers are collapsed and the higher-scored version is kept.
- Scoring: confirms papers with stronger keyword overlap score higher than unrelated papers.
- Relevance filtering: confirms weakly related papers, such as papers sharing only broad language-model terms but missing the main topic focus, are filtered out.
- Run isolation: confirms a second agent run does not include papers from a previous run.
- Reference validation: confirms accepted references must match retrieved paper titles, rejects invented references, and requires a references section.

## Test Result

The suite was run with:

```bash
.venv/bin/python -m pytest
```

Result: 11 tests passed.
