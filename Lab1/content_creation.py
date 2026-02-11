#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
YouTube Shorts Content Planner
------------------------------
This script utilizes CrewAI to automate the strategic planning of micro-history 
content. It defines a specialized agent to generate a 5-day content calendar 
optimized for high retention and engagement on short-form platforms.
"""

import os
import warnings
from crewai import Task, Agent, Crew
from patch import disable_ssl_verification
from utils import get_openai_api_key

# --- 1. Environment Configuration ---

# Disable SSL verification for specific network environments (e.g., Coursera)
disable_ssl_verification()

# Filter out non-critical warnings
warnings.filterwarnings('ignore')

# CrewAI internal testing flag and API Key initialization
os.environ["CREWAI_TESTING"] = "true"
os.environ["OPENAI_API_KEY"] = get_openai_api_key()

# --- 2. Agent Definition ---

# Define the 'Micro-History Strategist' agent.
# This agent is configured to prioritize high-retention hooks and 
# production feasibility for solo creators.
content_creator_assistant = Agent(
    role="YouTube Shorts Micro-History Strategist",
    goal="Plan a 1-week slate of high-retention YouTube Shorts about surprising origins of everyday things.",
    backstory=(
        "You are an expert in 30–45s micro-storytelling. Your specialty is "
        "crafting narratives that hook viewers within the first second, deliver "
        "a surprising historical twist, and maximize comment section engagement. "
        "All recommendations must be filmable by a solo creator with minimal equipment."
    ),
    llm="gpt-4o-mini",
    verbose=True
)

# --- 3. Task Definition ---

# Define the specific content creation task.
# The task requires a structured JSON output to ensure the data is 
# programmatically accessible and follows specific SEO/production criteria.
task = Task(
    description=( 
        "Create a 1-week video posting plan with 5 video blueprints. "
        "Platform: YouTube Shorts (vertical 9:16, 30-45s). "
        "Niche: Micro-History of Everyday Things. "
        "Requirements: 1) 1-second thumb-stop hook, 2) narrative twist, "
        "3) SEO-optimized titles, 4) engagement-focused Call to Action (CTA). "
        "Constraints: Home-filmable for a solo creator."
    ),
    expected_output=(
        '''
        A JSON array containing a weekly schedule of 5 video blueprints.
        Schema:
        {
          "videos": [
            {
              "title": "SEO title",
              "hook_main": "Opening line (max 12 words)",
              "hook_alt": "Alternative opening line",
              "visuals": ["List of simple prop or b-roll ideas"],
              "tags": ["#shorts", "#microhistory"],
              "cta": "Engagement question"
            }
          ]
        }
        '''
    ),
    agent=content_creator_assistant
)

# --- 4. Crew Assembly and Execution ---

# Assemble the agent and task into a crew. 
# While this is a single-agent workflow, the Crew structure allows for 
# future scalability (e.g., adding a separate 'Scriptwriter' or 'Researcher').
content_crew = Crew(
    agents=[content_creator_assistant],
    tasks=[task]
)

def run_content_planner():
    """Executes the CrewAI workflow and prints the resulting content plan."""
    print("🚀 Initiating content planning workflow...")
    
    result = content_crew.kickoff()
    
    print("\n" + "=" * 80)
    print("STRATEGIC WEEKLY CONTENT PLAN")
    print("=" * 80)
    print(result.raw)

if __name__ == "__main__":
    run_content_planner()