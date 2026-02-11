#!/usr/bin/env python
# coding: utf-8

# # Content Creation with CrewAI
# 
# Welcome to the first practice lab of this course!
# 
# In this lab , you'll see an example of using CrewAI for content creation. This demonstrates how to build a single-agent system for planning YouTube Shorts content.
# 
# **What you'll see:**
# - How to define an agent with a specific content creation role
# - How to create a task with structured output requirements
# - How to assemble an agent and task into a crew
# - How CrewAI executes the workflow
# 
# **What this example builds:**
# A **Content Planning Agent** that creates a weekly content calendar for YouTube Shorts focusing on micro-history topics.
# 
# ## Background
# 
# You're a content creator focusing on short-form video content about the surprising origins of everyday things. You want to create engaging 30-45 second YouTube Shorts that:
# - Hooks viewers in the first second
# - Tells a clear story with a surprising twist
# - Drives engagement through comments
# - Can be filmed at home with minimal equipment
# 
# Instead of manually brainstorming and planning content, you'll use an AI agent to generate a structured weekly content plan.
# 
# ## General instructions
# In this lab you will be presented with a structure of the code, but you will need to complete some of it. 
# 
# To successfully run this lab, replace all instances of the placeholder `None` with your own code. Sections where you need to write code will be delimited between `### START CODE HERE ###` and `### END CODE HERE ###`.
# 
# **<font color='#5DADEC'>Please make sure to save your work periodically, so you don't lose any progress.</font>**

# ## Table of Contents
# 
# - [1. Set Up Your Notebook](#1)
# - [2. Define the Content Planning Agent](#2)
# - [3. Define the Content Planning Task](#3)
# - [4. Create and Run the Crew](#4)
# - [5. Review the Results](#5)

# <a id="1"></a>
# 
# ## 1. Set Up Your Notebook
# 
# First, import the necessary modules and configure the environment.

# In[1]:


# Patch to disable SSL verification for Coursera
from patch import disable_ssl_verification
disable_ssl_verification()

import warnings
warnings.filterwarnings('ignore')


# In[2]:


from crewai import Task, Agent, Crew
import os
os.environ["CREWAI_TESTING"] = "true"
from utils import get_openai_api_key

os.environ["OPENAI_API_KEY"] = get_openai_api_key() 


# <a id="2"></a>
# 
# ## 2. Define the Content Planning Agent
# 
# Content creation is an excellent use case for AI agents because it involves:
# - **Strategy**: Understanding platform requirements and audience psychology
# - **Creativity**: Generating engaging hooks and concepts
# - **Structure**: Organizing content in a repeatable, scalable format
# 
# In this example, you'll create a single specialized agent:
# 
# **Content Planning Agent:**
# - Plans a weekly slate of video concepts
# - Ensures each video follows best practices for retention
# - Keeps ideas practical and filmable for a solo creator
# 
# The agent will produce a structured JSON output with video blueprints that include titles, hooks, visual ideas, tags, and calls-to-action.
# 
# Agents in CrewAI represent team members with specific roles, goals, and expertise. Each agent has:
# - **Role**: Their job title or function
# - **Goal**: What they aim to achieve
# - **Backstory**: Their experience and expertise. This helps the LLM understand how to roleplay the agent.
# - **LLM**: The language model to use (in this case, gpt-4o-mini)
# - **Verbose**: Whether to show detailed output (useful for learning and debugging)
# 
# Use the next cell to create your very own agent! Try following best practices, as shown by João.

# In[3]:


# Define the Content Planning Agent
content_creator_assistant = Agent(
    role="YouTube Shorts Micro-History Strategist",
    goal="Plan a 1-week slate of high-retention YouTube Shorts about surprising origins of everyday things.",
    backstory=(
        "You specialize in 30–45s micro-history that hooks fast, pays off with a twist, and drives comments. "
        "You keep ideas filmable by a solo creator at home with minimal props."
    ),
    llm="gpt-4o-mini",
    verbose=True
)

print("✓ Content planning agent defined")


# <a id="3"></a>
# 
# ## 3. Define the Content Planning Task
# 
# Tasks define the actual work that agents will perform. Each task has:
# - **Description**: What needs to be done, including context and requirements
# - **Expected Output**: What the result should look like (in this case, a JSON schema)
# - **Agent**: Which agent will perform this task
# 
# Let's create a task that generates a weekly content plan with structured video blueprints. Once again, try using best practices to fill in the fields.

# In[4]:


# Define the Content Planning Task
task = Task(
    description=( 
        "Create a 1-week video posting plan with 5 video blueprints. "
        "Platform: YouTube Shorts (vertical 9:16, 30-45s). "
        "Niche: Micro-History of Everyday Things (e.g., why pencils are yellow, origins of bubble wrap, etc.). "
        "Primary goals: 1) thumb-stop hook in first 1s, 2) crystal-clear narrative with a surprise, "
        "3) strong SEO phrasing in title/caption, 4) comment-bait CTA. "
        "Context: solo creator, home-filmable, no special gear. "
    ),
    expected_output=(
        '''
        Output a JSON array following the schema below, which contains a
        weekly schedule and 5 video blueprints. Each video blueprint should include:
        {
          "videos": [
            {
              "title": "<searchable, curiosity-driven title>",
              "hook_main": "<<=12 words, shows payoff fast>",
              "hook_alt": "<variant hook>",
              "visuals": ["simple prop or b-roll idea 1", "idea 2"],
              "tags": ["#microhistory","#everydaythings","#shorts"],
              "cta": "<question that invites comments>"
            }
          ]
        }
        '''
    ),
    agent=content_creator_assistant
)

print("✓ Content planning task defined")


# <a id="4"></a>
# 
# ## 4. Create and Run the Crew
# 
# Now you'll assemble the agent and task into a **Crew**. Even with a single agent, CrewAI provides a structured way to organize and execute the workflow.
# 
# The crew will:
# 1. Execute the task using the agent
# 2. Use the LLM to power agent reasoning and content generation
# 3. Return structured output according to the expected format

# In[5]:


# Create the content planning crew
crew = Crew(
    agents=[content_creator_assistant],
    tasks=[task]
)

print("✓ Content planning crew created")
print("\n🚀 Starting content planning...\n")

# Execute the crew's task
result = crew.kickoff()

print("\n✓ Content planning complete!")


# <a id="5"></a>
# 
# ## 5. Review the Results
# 
# Let's examine the output from the content planning task. The agent should have generated a structured JSON with 5 video blueprints for the week.

# In[6]:


# Display the content plan
print("=" * 80)
print("WEEKLY CONTENT PLAN")
print("=" * 80)
print(result.raw)


# 
# 
# Congratulations! You've successfully finished this lab. See you in the next one. 🚀
