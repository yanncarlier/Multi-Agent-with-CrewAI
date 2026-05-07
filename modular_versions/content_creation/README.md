# modular_versions/content_creation

## What’s in this module
Modular, configuration-driven version of the **YouTube Shorts content planning** workflow.

### Program: `content_creation_modular.py`
This script:
- Loads **Agent** and **Task** prompts from markdown files in:
  - `agent_definitions/`
  - `task_definitions/`
- Builds a CrewAI workflow and runs it to generate a content plan.

#### Run
From the repository root:

```bash
python modular_versions/content_creation/content_creation_modular.py
```

#### Output
Prints the resulting plan to stdout.

#### Notes
- Expects an appropriate `.env` (handled in `utils.py`).
- Uses `modular_versions/content_creation/patch.py` to disable SSL verification in constrained environments.

