# modular_versions/agents_automatic_code_review

## What’s in this module
Modular, configuration-driven version of the **automated code review** workflow.

### Program: `agents_automatic_code_review_modular.py`
This script implements a 3-agent flow:
- **Senior Developer**: bug/style/maintainability triage (critical vs minor).
- **Security Engineer**: security vulnerability review using OWASP guidance (via Serper + scraping).
- **Tech Lead**: final decision (approve / request changes / escalate).

Agent and task prompt configuration is loaded from markdown files in:
- `agent_definitions/`
- `task_definitions/`

#### Run
From the repository root:

```bash
python modular_versions/agents_automatic_code_review/agents_automatic_code_review_modular.py
```

#### Inputs / outputs
- Input: `modular_versions/agents_automatic_code_review/code_changes.txt`
- Output: saves a serialized run result to `modular_versions/agents_automatic_code_review/results.dill`
- Printed: the final Tech Lead report

#### Notes
- Expects an appropriate `.env` (handled in `utils.py`).
- Uses `modular_versions/agents_automatic_code_review/patch.py` to disable SSL verification in constrained environments.

