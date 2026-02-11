# main.py

import os
import dill
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from patch import disable_ssl_verification
from utils import get_openai_api_key, get_serper_api_key

# --- Environment Setup ---

# Disable SSL verification for specific environment compatibility
disable_ssl_verification()

# Configure environment variables for CrewAI and LLM
os.environ["CREWAI_TESTING"] = "true"
os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["MODEL"] = "Llama-3.2-3B-Instruct-Q4_K_M"
os.environ["DLAI_SERPER_BASE_URL"] = os.getenv("DLAI_SERPER_BASE_URL")

# --- Resource Loading ---

# Load the pull request code changes for analysis
with open('code_changes.txt', 'r') as file:
    code_changes = file.read()

# --- Tool Initialization ---

# Search tool configured specifically for OWASP security documentation
serper_search_tool = SerperDevTool(
    search_url="https://owasp.org", 
    base_url=os.getenv("DLAI_SERPER_BASE_URL")
)

# Tool for extracting detailed content from identified URLs
scrape_website_tool = ScrapeWebsiteTool()

# --- Agent Definitions ---

# Focuses on bugs, style, and maintainability
senior_developer = Agent(
    role="Senior Developer",
    goal="Evaluate code changes to identify bugs, style, and maintainability issues; triage findings and decide which issues must be fixed before approval (classify issues as critical vs. minor).",
    backstory="Senior software engineer with extensive experience reviewing and maintaining large codebases. Expert at prioritizing fixes, enforcing coding standards, and distinguishing blocking defects from minor stylistic suggestions.",
    verbose=True,
)

# Focuses on identifying vulnerabilities using OWASP resources
security_engineer = Agent(
    role="Security Engineer",
    goal="Identify vulnerabilities in code and determine their risk levels and potential impact on the application",
    backstory=( 
        "You are an expert Security Engineer with deep knowledge of code security vulnerabilities. "
        "Your responsibility is to thoroughly analyze code for security flaws and make critical decisions "
        "about the severity and potential impact of security concerns. You evaluate code quality from a "
        "security perspective and provide actionable recommendations for addressing vulnerabilities."
    ),
    verbose=True,
    tools=[serper_search_tool, scrape_website_tool],
)

# Orchestrates the final decision based on developer and security feedback
tech_lead = Agent(
    role="Tech Lead",
    goal="Evaluate code quality and security findings to determine if changes can be automatically approved, identify required fixes, or escalate for human review",
    backstory=(
            "You are an experienced Tech Lead with expertise in managing code review workflows. "
            "Your responsibility is to make final decisions about pull request approvals based on "
            "findings from your team. You balance code quality concerns with security requirements, "
            "distinguish blocking issues from minor improvements, and decide the appropriate path "
            "forward for each change: automatic approval, request for fixes, or escalation to human review."
        ),
    verbose=True,
)

# --- Task Definitions ---

# Task 1: Quality Analysis
analyze_code_quality = Task(
    description=( 
        "Review the following code changes for quality issues:\n\n{code_changes}\n\n"
        "Your task is to:\n"
        "1. Analyze the code for potential bugs, style issues, and maintainability concerns\n"
        "2. Identify any problems that could impact functionality or code quality\n"
        "3. Classify each issue as either CRITICAL (must be fixed before approval) or MINOR (suggested improvements)\n"
        "4. Provide clear reasoning for your classifications\n\n"
        "Focus on determining which issues are blocking problems versus nice-to-have improvements."
    ),
    expected_output=(
        "A JSON object with the following structure:\n"
        "{\n"
        "  \"critical_issues\": [array of issues that must be fixed before approval],\n"
        "  \"minor_issues\": [array of suggested improvements that are not blocking],\n"
        "  \"reasoning\": string explaining the rationale for classifications\n"
        "}"
    ),
    name="Analyze Code Quality",
    agent=senior_developer
)

# Task 2: Security Review
review_security = Task(
    description=( 
        "Review the following code changes for security vulnerabilities:\n\n{code_changes}\n\n"
        "Your task is to:\n"
        "1. Examine the code for potential security vulnerabilities and weaknesses\n"
        "2. Identify all security issues and classify them by risk level (Critical, High, Medium, Low)\n"
        "3. Determine which issues are blocking (prevent approval) versus non-blocking\n"
        "4. Provide specific recommendations for fixing each vulnerability\n\n"
        "Use the SerperDevTool to find the most relevant security best practices from OWASP "
        "and pass the URLs to the ScrapeWebsiteTool to get detailed information."
    ),
    expected_output=( 
        "A JSON object with the following structure:\n"
        "{\n"
        "  \"security_vulnerabilities\": [array of identified issues with risk levels],\n"
        "  \"blocking\": boolean indicating if security issues should block approval,\n"
        "  \"highest_risk\": the most severe risk level found,\n"
        "  \"security_recommendations\": [specific fixes for vulnerabilities]\n"
        "}"
    ),
    agent=security_engineer,
    name="Review Security",
)

# Task 3: Decision making (Uses context from previous tasks)
make_review_decision = Task(
    description=( 
        "Review the code changes and determine if the PR can be approved. "
        "Code changes to review:\n{code_changes}\n\n"
        "Your task is to:\n"
        "1. Analyze the code changes provided\n"
        "2. Determine if the PR meets approval criteria\n"
        "3. Decide on next steps (approve, request changes, or escalate)\n"
        "4. Explain your decision with clear reasoning"
    ),
    expected_output=(
        "A short report that includes:\n"
        "- Final decision (approve, request changes, or escalate)\n"
        "- Required changes (if any)\n"
        "- Approval comments (if approving)\n"
        "- Escalation reasoning (if escalating)\n"
        "- Additional recommendations"
    ), 
    agent=tech_lead,
    context=[analyze_code_quality, review_security],
    name="Review Decision",
)

# --- Crew Execution ---

# Assemble the multi-agent team
code_review_crew = Crew(
    agents=[security_engineer, senior_developer, tech_lead],
    tasks=[review_security, analyze_code_quality, make_review_decision],
)

# Define inputs and start the process
inputs = {"code_changes": code_changes}
result = code_review_crew.kickoff(inputs=inputs)

# --- Post-Processing ---

# Save the execution results for evaluation
with open("results.dill", "wb") as f:
    dill.dump(result, f)

# Display the final Tech Lead report
print("\n--- Final Review Report ---\n")
print(result.tasks_output[2].raw)