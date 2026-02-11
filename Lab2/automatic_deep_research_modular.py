# automatic_deep_research.py

import os
import re
from pathlib import Path
from crewai import Agent, Task, Crew
from crewai_tools import EXASearchTool, ScrapeWebsiteTool
from IPython.display import Markdown

# Importing custom utilities
from patch import disable_ssl_verification
from utils import get_openai_api_key, get_exa_api_key

# --- Environment Setup ---
disable_ssl_verification()

os.environ["CREWAI_TESTING"] = "true"
os.environ["MODEL"] = "Llama-3.2-3B-Instruct-Q4_K_M"
os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["EXA_API_KEY"] = get_exa_api_key()

# --- Helper Function to Load MD Content ---

def load_md_content(file_path):
    """Parses MD files to extract labeled sections for Agents and Tasks."""
    content = Path(file_path).read_text()
    
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

# --- Tool Initialization ---
exa_search_tool = EXASearchTool(base_url=os.getenv("EXA_BASE_URL"))
scrape_website_tool = ScrapeWebsiteTool()

# --- Load Configurations ---
# Agents
planner_cfg = load_md_content("agent_definitions/research_planner.md")
researcher_cfg = load_md_content("agent_definitions/researcher.md")
checker_cfg = load_md_content("agent_definitions/fact_checker.md")
writer_cfg = load_md_content("agent_definitions/report_writer.md")

# Tasks
plan_task_cfg = load_md_content("task_definitions/create_research_plan.md")
data_task_cfg = load_md_content("task_definitions/gather_research_data.md")
verify_task_cfg = load_md_content("task_definitions/verify_information_quality.md")
report_task_cfg = load_md_content("task_definitions/write_final_report.md")

# --- Agent Definitions ---
research_planner = Agent(
    role=planner_cfg["role"],
    goal=planner_cfg["goal"],
    backstory=planner_cfg["backstory"],
    verbose=True,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

researcher = Agent(
    role=researcher_cfg["role"],
    goal=researcher_cfg["goal"],
    backstory=researcher_cfg["backstory"],
    tools=[exa_search_tool, scrape_website_tool],
    verbose=True,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

fact_checker = Agent(
    role=checker_cfg["role"],
    goal=checker_cfg["goal"],
    backstory=checker_cfg["backstory"],
    tools=[exa_search_tool, scrape_website_tool],
    verbose=True,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

report_writer = Agent(
    role=writer_cfg["role"],
    goal=writer_cfg["goal"],
    backstory=writer_cfg["backstory"],
    verbose=True,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

# --- Task Definitions ---
create_research_plan_task = Task(
    description=plan_task_cfg["description"],
    expected_output=plan_task_cfg["expected_output"],
    agent=research_planner,
)

gather_research_data_task = Task(
    description=data_task_cfg["description"],
    expected_output=data_task_cfg["expected_output"],
    agent=researcher
)

verify_information_quality_task = Task(
    description=verify_task_cfg["description"],
    expected_output=verify_task_cfg["expected_output"],
    agent=fact_checker
)

write_final_report_task = Task(
    description=report_task_cfg["description"],
    expected_output=report_task_cfg["expected_output"],
    agent=report_writer
)

# --- Crew Execution ---
deep_research_crew = Crew(
    agents=[research_planner, researcher, fact_checker, report_writer],
    tasks=[
        create_research_plan_task, 
        gather_research_data_task, 
        verify_information_quality_task, 
        write_final_report_task
    ]
)

query = "The impact of generative AI on software engineering productivity in 2025"

print(f"### Initializing Deep Research for: {query} ###")
result = deep_research_crew.kickoff(inputs={'user_query': query})

print("\n" + "="*50 + "\nFINAL REPORT\n" + "="*50)
print(result.raw)