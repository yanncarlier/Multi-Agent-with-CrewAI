# automatic_deep_research.py

import os
from crewai import Agent, Task, Crew
from crewai_tools import EXASearchTool, ScrapeWebsiteTool
from IPython.display import Markdown

# -----------------------------------------------------------------
# 1. Configuration & Environment Setup
# -----------------------------------------------------------------
# Importing custom utilities for API keys and SSL management
from patch import disable_ssl_verification
from utils import get_openai_api_key, get_exa_api_key

# Disable SSL verification for specific network environments
disable_ssl_verification()

# Environment Variables Configuration
os.environ["CREWAI_TESTING"] = "true"
os.environ["MODEL"] = "Llama-3.2-3B-Instruct-Q4_K_M"
os.environ["OPENAI_API_KEY"] = get_openai_api_key()
os.environ["EXA_API_KEY"] = get_exa_api_key()

# -----------------------------------------------------------------
# 2. Tool Initialization
# -----------------------------------------------------------------
# EXASearchTool: Semantic search across the web via exa.ai
exa_search_tool = EXASearchTool(base_url=os.getenv("EXA_BASE_URL"))

# ScrapeWebsiteTool: Content extraction from specific URLs
scrape_website_tool = ScrapeWebsiteTool()

# -----------------------------------------------------------------
# 3. Agent Definitions
# -----------------------------------------------------------------

# Research Planner: Deconstructs complex queries into actionable roadmaps
research_planner = Agent(
    role="Research Planner",
    goal="Analyze queries and break them down into smaller, specific research topics.",
    backstory=(
        "You are a strategic analyst specializing in information architecture. "
        "Your expertise lies in identifying core research objectives and "
        "organizing complex questions into logical investigative paths."
    ),
    verbose=True,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

# Internet Researcher: Executes data gathering using specialized web tools
researcher = Agent(
    role="Internet Researcher",
    goal="Perform thorough investigations on all assigned research topics.",
    backstory=(
        "You are a digital sleuth with advanced skills in navigating the modern web. "
        "You excel at surfacing high-quality data and primary sources while "
        "maintaining focus on technical accuracy."
    ),
    tools=[exa_search_tool, scrape_website_tool],
    verbose=True,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

# Fact Checker: Validates research integrity and cross-references data
fact_checker = Agent(
    role="Fact Checker",
    goal="Verify data for accuracy, identify inconsistencies, and flag misinformation.",
    backstory=(
        "You are a meticulous auditor with a focus on data integrity. "
        "You apply rigorous cross-referencing techniques to ensure all "
        "gathered information is reliable and provides a single version of truth."
    ),
    tools=[exa_search_tool, scrape_website_tool],
    verbose=True,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

# Report Writer: Synthesizes findings into professional documentation
report_writer = Agent(
    role="Report Writer",
    goal="Synthesize verified information into structured, professional reports.",
    backstory=(
        "You are a technical writer expert at translating complex datasets "
        "into clear, actionable insights. Your style is professional, "
        "evidence-based, and highly structured."
    ),
    tools=[], 
    verbose=True,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)

# -----------------------------------------------------------------
# 4. Task Definitions
# -----------------------------------------------------------------

# Task 1: Generate the Strategic Research Plan
create_research_plan_task = Task(
    description=(
        "Analyze the following query and develop a comprehensive research plan "
        "including key topics, investigative questions, and success metrics. "
        "Query: {user_query}"
    ),
    expected_output=(
        "A structured research plan document containing main investigation "
        "topics, specific questions per topic, and defined success criteria."
    ),
    agent=research_planner,
)

# Task 2: Data Acquisition
gather_research_data_task = Task(
    description=(
        "Execute the research plan by gathering data across the internet. "
        "Ensure every piece of information is mapped to a verified source URL."
    ),
    expected_output=(
        "A comprehensive dataset of findings grouped by topic, including "
        "full source citations and initial credibility notes for each link."
    ),
    agent=researcher
)

# Task 3: Quality Assurance and Verification
verify_information_quality_task = Task(
    description=(
        "Audit the gathered research for conflicting data points or "
        "potential misinformation. Close any information gaps discovered."
    ),
    expected_output=(
        "A verification report highlighting consistent data, resolved "
        "contradictions, and reliability ratings for the sources used."
    ),
    agent=fact_checker
)

# Task 4: Final Synthesis and Reporting
write_final_report_task = Task(
    description=(
        "Synthesize all verified research into a final executive report. "
        "The report must be professional, cited, and address the original query."
    ),
    expected_output=(
        "A complete research report featuring an executive summary, "
        "detailed analytical sections, actionable insights, and a bibliography."
    ),
    agent=report_writer
)

# -----------------------------------------------------------------
# 5. Crew Execution
# -----------------------------------------------------------------

# Assemble the agents and tasks into a sequential workflow
deep_research_crew = Crew(
    agents=[
        research_planner, 
        researcher, 
        fact_checker, 
        report_writer
    ],
    tasks=[
        create_research_plan_task, 
        gather_research_data_task, 
        verify_information_quality_task, 
        write_final_report_task
    ]
)

# Define the research query
query = "The impact of generative AI on software engineering productivity in 2025"

# Execute the workflow
print(f"### Initializing Deep Research for: {query} ###")
result = deep_research_crew.kickoff(inputs={'user_query': query})

# Render the final output
print("\n" + "="*50 + "\nFINAL REPORT\n" + "="*50)
Markdown(result.raw)