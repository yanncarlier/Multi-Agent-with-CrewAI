# Task: Review Security

**Description:**
Review the following code changes for security vulnerabilities:

{code_changes}

Your task is to:
1. Examine the code for potential security vulnerabilities and weaknesses
2. Identify all security issues and classify them by risk level (Critical, High, Medium, Low)
3. Determine which issues are blocking (prevent approval) versus non-blocking
4. Provide specific recommendations for fixing each vulnerability

Use the SerperDevTool to find the most relevant security best practices from OWASP and pass the URLs to the ScrapeWebsiteTool to get detailed information.

**Expected Output:**
A JSON object with the following structure:
{
  "security_vulnerabilities": [array of identified issues with risk levels],
  "blocking": boolean indicating if security issues should block approval,
  "highest_risk": the most severe risk level found,
  "security_recommendations": [specific fixes for vulnerabilities]
}