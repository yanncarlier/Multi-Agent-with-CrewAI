# modular_versions/automatic_deep_research

## What’s in this module
Modular, configuration-driven version of **automatic deep research**.

### Program: `automatic_deep_research_modular.py`
This script performs a sequential multi-agent workflow:
1. Create a research plan.
2. Gather research data from the web (Exa search + website scraping).
3. Verify information quality / resolve inconsistencies.
4. Write the final report.

Agent + task instructions are loaded from markdown files in:
- `agent_definitions/`
- `task_definitions/`

#### Run
From the repository root:

```bash
python modular_versions/automatic_deep_research/automatic_deep_research_modular.py
```

#### Output
Prints the final report (and renders it as markdown in-notebook contexts via `IPython.display`).

#### Notes
- Expects an appropriate `.env` (handled in `utils.py`) including OpenAI/Exa keys.
- Uses `modular_versions/automatic_deep_research/patch.py` to disable SSL verification in constrained environments.

