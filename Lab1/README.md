# Lab1

## What’s in this lab
This folder contains a CrewAI-based workflow for **planning YouTube Shorts**.

### Program: `content_creation.py`
A single-agent CrewAI script that:
- Loads agent/task instructions from markdown files (`agent_definitions/` and `task_definitions/`).
- Runs the workflow and prints a structured content plan.

#### Run
From the repository root:

```bash
python Lab1/content_creation.py
```

#### Requirements / configuration
- Expects a `.env` file one directory above the lesson path (see `Lab1/utils.py`).
- Uses `OPENAI_API_KEY` (and SSL patching via `Lab1/patch.py`).

