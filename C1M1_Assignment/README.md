# C1M1 Assignment

## What’s in this assignment
This folder contains a **multi-agent automated code review** workflow built with CrewAI.

### Program: `agents_automatic_code_review.py`
A 3-agent workflow that evaluates a set of code changes and decides whether a pull request should be:
- approved,
- request changes, or
- escalated to human review.

#### How it works
It loads code changes from `code_changes.txt`, then runs:
1. **Senior Developer**: bug/style/maintainability triage; classifies findings as **CRITICAL** vs **MINOR**.
2. **Security Engineer**: identifies security vulnerabilities and risk levels (Critical/High/Medium/Low) using OWASP as guidance.
3. **Tech Lead**: synthesizes both reviews and makes a final decision.

#### Run
From the repository root:

```bash
python C1M1_Assignment/agents_automatic_code_review.py
```

#### Inputs / outputs
- Input: `C1M1_Assignment/code_changes.txt`
- Output: saves a serialized run result to `C1M1_Assignment/results.dill`
- Printed: the final Tech Lead report (from `result.tasks_output[2].raw`).

#### Requirements / configuration
- Expects a `.env` file (see `C1M1_Assignment/utils.py`).
- Uses `OPENAI_API_KEY` and `SERPER`/Scraping settings (via `SerperDevTool`).
- Uses `C1M1_Assignment/patch.py` to disable SSL verification in some network environments.

