# Task: Analyze Code Quality

**Description:**
Review the following code changes for quality issues:

{code_changes}

Your task is to:
1. Analyze the code for potential bugs, style issues, and maintainability concerns
2. Identify any problems that could impact functionality or code quality
3. Classify each issue as either CRITICAL (must be fixed before approval) or MINOR (suggested improvements)
4. Provide clear reasoning for your classifications

Focus on determining which issues are blocking problems versus nice-to-have improvements.

**Expected Output:**
A JSON object with the following structure:
{
  "critical_issues": [array of issues that must be fixed before approval],
  "minor_issues": [array of suggested improvements that are not blocking],
  "reasoning": string explaining the rationale for classifications
}