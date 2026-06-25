# Remediation Log

## 1. Command-Line Argument Mismatch

Issue: An early command used `--max-papers`, but the implemented CLI used `--papers-per-subgoal`.

Resolution: The project documentation and usage now reflect the implemented command-line option, `--papers-per-subgoal`, which controls how many OpenAlex papers are retrieved for each planned subgoal.

## 2. Previous-Run Papers Appeared in Later Outputs

Issue: SQLite originally retained papers from earlier runs. As a result, a later topic could include references retrieved for a previous topic.

Resolution: The store is now cleared at the start of each agent run. This keeps each command-line run isolated and ensures the final literature review only uses papers retrieved and processed for the current topic.

## 3. Weakly Relevant Papers Appeared in the Review

Issue: Some papers with only broad keyword overlap, such as healthcare education or financial sentiment analysis papers, could appear for the topic "large language model agents."

Resolution: Relevance scoring was strengthened to depend more heavily on overlap between the topic words, subgoal words, and the paper title or abstract. A minimum relevance threshold now filters weak papers before the literature review is generated.

## 4. Non-Failing macOS urllib3 Warning

Issue: Running tests on macOS Python shows a `urllib3` warning about LibreSSL support.

Resolution: This warning does not cause test or execution failure. The pytest suite still passes successfully, and the application behavior is unaffected.
