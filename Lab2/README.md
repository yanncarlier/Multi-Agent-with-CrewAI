# Lab2

## What’s in this lab
This folder contains a CrewAI-based workflow for **automatic deep research**.

### Program: `automatic_deep_research.py`
A multi-agent sequential workflow that:
1. Plans research topics from a user query.
2. Gathers data from the web (Exa search + website scraping).
3. Fact-checks and validates gathered information.
4. Writes a final executive-style report.

#### Run
From the repository root:

```bash
python Lab2/automatic_deep_research.py
```

#### Notes
- Uses `Lab2/utils.py` to load `OPENAI_API_KEY` and `EXA_API_KEY` from `.env`.
- Uses `Lab2/patch.py` to disable SSL verification for constrained network environments.
- The default query is embedded in the script.

