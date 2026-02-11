# agents_automatic_code_review.py

import os
import dill
import re
from pathlib import Path
from crewai import Agent, Task, Crew
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from patch import disable_ssl_verification
from utils import get_openai_api_key, get_serper_api_key

# --- Environment Setup ---
disable_ssl_verification()
os.environ["CREWAI_TESTING"] = "true"
os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["MODEL"] = "Llama-3.2-3B-Instruct-Q4_K_M"
os.environ["DLAI_SERPER_BASE_URL"] = os.getenv("DLAI_SERPER_BASE_URL")

# --- Resource Loaders ---

def load_md_content(file_path):
    """Parses MD files to extract labeled sections."""
    content = Path(file_path).read_text()
    
    # Helper to find text between a label and the next label/end of file
    def extract_section(label, text):
        pattern = rf"\*\*{label}:\*\*\s*([\s\S]*?)(?=\n\n\*\*|\Z)"
        match = re.search(pattern, text)
        return match.group(1).strip() if match else ""

    return {
        "role": extract_section("Role", content),
        "goal": extract_section("Goal", content),
        "backstory": extract_section("Backstory", content),
        "description": extract_section("Description", content),
        "expected_output": extract_section("Expected Output", content)
    }

# Load the pull request code changes
with open('code_changes.txt', 'r') as file:
    code_changes = file.read()

# Load configurations
senior_dev_cfg = load_md_content("agent_definitions/senior_developer.md")
security_eng_cfg = load_md_content("agent_definitions/security_engineer.md")
tech_lead_cfg = load_md_content("agent_definitions/tech_lead.md")

task_quality_cfg = load_md_content("task_definitions/analyze_code_quality.md")
task_security_cfg = load_md_content("task_definitions/review_security.md")
task_decision_cfg = load_md_content("task_definitions/make_review_decision.md")

# --- Tool Initialization ---
serper_search_tool = SerperDevTool(
    search_url="https://owasp.org", 
    base_url=os.getenv("DLAI_SERPER_BASE_URL")
)
scrape_website_tool = ScrapeWebsiteTool()

# --- Agent Definitions ---
senior_developer = Agent(
    role=senior_dev_cfg["role"],
    goal=senior_dev_cfg["goal"],
    backstory=senior_dev_cfg["backstory"],
    verbose=True
)

security_engineer = Agent(
    role=security_eng_cfg["role"],
    goal=security_eng_cfg["goal"],
    backstory=security_eng_cfg["backstory"],
    verbose=True,
    tools=[serper_search_tool, scrape_website_tool]
)

tech_lead = Agent(
    role=tech_lead_cfg["role"],
    goal=tech_lead_cfg["goal"],
    backstory=tech_lead_cfg["backstory"],
    verbose=True
)

# --- Task Definitions ---
analyze_code_quality = Task(
    description=task_quality_cfg["description"],
    expected_output=task_quality_cfg["expected_output"],
    name="Analyze Code Quality",
    agent=senior_developer
)

review_security = Task(
    description=task_security_cfg["description"],
    expected_output=task_security_cfg["expected_output"],
    agent=security_engineer,
    name="Review Security"
)

make_review_decision = Task(
    description=task_decision_cfg["description"],
    expected_output=task_decision_cfg["expected_output"],
    agent=tech_lead,
    context=[analyze_code_quality, review_security],
    name="Review Decision"
)

# --- Crew Execution ---
code_review_crew = Crew(
    agents=[security_engineer, senior_developer, tech_lead],
    tasks=[review_security, analyze_code_quality, make_review_decision],
)

inputs = {"code_changes": code_changes}
result = code_review_crew.kickoff(inputs=inputs)

# --- Post-Processing ---
with open("results.dill", "wb") as f:
    dill.dump(result, f)

print("\n--- Final Review Report ---\n")
print(result.tasks_output[2].raw)