#!/usr/bin/env python
# coding: utf-8

# # Automatic Deep Research 
# 
# Welcome to this new practice lab! By now you should have a clearer view of the elements that compose a multi-agent system. In this lab you will get to put it into action by creating your first crew.
# 
# **What you'll learn:**
# - How to define agents with specific roles and expertise
# - How to provide agents with tools to perform their tasks
# - How to create your own tasks that agents will execute
# - How to assemble agents and tasks into a Crew, all using CrewAI
# 
# ## Background
# 
# As a research consultant, you're constantly tasked with producing comprehensive reports on diverse topics for demanding clients. You need to build an automatic deep research solution that can rapidly gather, verify, and synthesize information from across the internet, delivering reliable, fact-checked reports that meet tight deadlines and exacting standards regardless of the subject matter. 
# 
# ## General instructions
# In this lab you will be presented with a structure of the code, but you will need to complete some of it. 
# 
# To successfully run this lab, replace all instances of the placeholder `None` with your own code. Sections where you need to write code will be delimited between `### START CODE HERE ###` and `### END CODE HERE ###`.
# 
# If you are stuck, or simply want to copy a solution into your notebook so that you can execute it, you can find all solution code inside the [Solution](Solution) folder.
# 
# **<font color='#5DADEC'>Please make sure to save your work periodically, so you don't lose any progress.</font>**

# ## Table of contents
# 
# - [1. Understanding the problem](#1)
# - [2. Set up your notebook](#2)
# - [3. Define the Agents](#3)
#   - [3.1. Create tool instances](#3-1)
#   - [3.2. Define the Research Planner agent](#3-2)
#   - [3.3. Define the remaining agents](#3-3)
# - [4. Create the Tasks](#4)
#   - [4.1. Define the Create research plan task](#4-1)
#   - [4.2. Define the remaining tasks](#4-2)
# - [5. Define the Crew and get the results](#5)

# <a id="1"></a>
# 
# ## 1. Understanding the problem
# In this lab, you will focus on building a custom deep research crew. This Crew will be in charge of creating a research plan based on the user's input, and executing it, while reviewing and checking the facts. Finally, with the gathered information a report needs to be generated.
# 
# Take some time to decompose the problem into different tasks. Who would be the appropriate "person" to solve each task? 
# 
# Once you've done your thinking, click below to find an agent/task diagram for this lab.    
# 
# 
# <details>    
# <summary>
#     <font size="3" color="#237b946b"><b>Diagram</b></font>
# </summary>
# 
# <img src="../images/lab2-agents-tasks-diagram.PNG">

# <a id="2"></a>
# 
# ## 2. Set up your notebook
# 
# Before you start coding, run the next two cells to import all necessary modules and configure the environment variables. 

# In[ ]:


# Patch to disable SSL verification for Coursera
from patch import disable_ssl_verification
disable_ssl_verification()

from crewai import Agent, Task, Crew
import os
os.environ["CREWAI_TESTING"] = "true"
from utils import get_openai_api_key

# set the OpenAI model (Llama-3.2-3B-Instruct-Q4_K_M)
os.environ["MODEL"] = "Llama-3.2-3B-Instruct-Q4_K_M"
# set up the OpenAI API key 
os.environ["OPENAI_API_KEY"] = get_openai_api_key()


# <a id="3"></a>
# 
# ## 3. Define the Agents
# 
# Based on the diagram, you should have four agents:
# - **Research Planner**: its goal is to analyze queries and break them down into smaller, specific research topics.
# - **Internet Researcher**: its job is to perform research tasks.
# - **Fact checker**: its goal is to review information for fact accuracy to avoid misinformation. 
# - **Report Writer**: is in charge of writing reports, based on gathered information.
# 
# <a id="3-1"></a>
# 
# ### 3.1. Create tool instances
# As you can see in the diagram, you will be providing the **Internet Researcher Agent** with tools, so that it can better do their job. In particular, you will give this agent access to search the internet and scrape information from the retrieved webpages. 
# 
# There are different tools inside CrewAI you can use to search the web, in this lab you will use the [**EXA Search Web Loader**](https://docs.crewai.com/en/tools/search-research/exasearchtool#exa-search-web-loader) tool, which is designed to perform a semantic search for a specified query from a text’s content across the internet. It utilizes the [exa.ai](https://exa.ai/) API to fetch and display the most relevant search results based on the query provided by the user. exa.ai enhances semantic search by capturing richer contextual relationships between concepts, allowing for more precise information retrieval than conventional embedding approaches.
# 
# For webscraping, you will use the [**Scrape Website**](https://docs.crewai.com/en/tools/web-scraping/scrapewebsitetool) tool, which is designed to extract and read the content of a specified website.
# 
# In the next cell you will define instances of these tools, so you can later assign them to the agents.

# In[ ]:


# import the tools
from crewai_tools import EXASearchTool, ScrapeWebsiteTool
from utils import get_exa_api_key

# set the exa API key
os.environ["EXA_API_KEY"] = get_exa_api_key()

### START CODE HERE ###

# # Create the EXASearchTool instance
# exa_search_tool = None(base_url=os.getenv("EXA_BASE_URL"))
# # Create the ScrapeWebsiteTool instance
# scrape_website_tool = None()

exa_search_tool = EXASearchTool(base_url=os.getenv("EXA_BASE_URL"))
scrape_website_tool = ScrapeWebsiteTool()

### END CODE HERE ###


# <a id="3-2"></a>
# 
# ### 3.2. Define the Research Planner agent
# 
# In the cell below, you will see how you can create the first agent. This time, all the parameters are set up for you. Here is a quick recap of what each of the parameters represent:
# 
# - `Role`: If this was a person doing the job, what title would they have?
# - `Goal`: What is the goal this agent in particular is trying to accomplish? Make sure to write concrete goal
# - `Background`: it should be something the highlights the skills of the agent relevant to its role. Make sure to use keywords that will actually help your agent get better results.
# 
# In the labs, we have added two parameters not shown in the demo videos: `max_rpm`, and `max_iter`. `max_rpm` sets the maximum requests per minute to avoid rate limits, while `max_iter` limits the maximum iterations before the agent must provide its best answer. Setting these two parameters helps make the agents run a little faster, so the lab doesn't take as long to complete. 

# In[ ]:


# define the research planner agent
research_planner = Agent(
    role="Research Planner",
    goal="Analyze queries and break them down into smaller, specific research topics.",
    backstory=(
         "You are a research strategist who excels at breaking down complex questions "
         "into manageable research components. You identify what needs to be researched "
         "and create clear research objectives."
    ),
    verbose=True,
    max_iter=2,   # Load reduction: stop after 3 attempts to find info
    max_rpm=10,   # Load reduction: slow down requests to avoid 503 errors
    allow_delegation=False # Load reduction: don't let it start new sub-tasks
)


# <a id="3-3"></a>
# 
# ### 3.3. Define the remaining agents
# 
# Now you can define the three remaining agents. The `role` and `goal` parameters are already filled in for you; use your own creativity to fill in the `backstory`.  
# 
# Do not forget to assign the tools to the **Internet Researcher** and **Fact Checker** agents. You can do this by setting the `tools` argument.

# In[ ]:


# Define the Internet Researcher
researcher = Agent(
    role="Internet Researcher",
    goal="Research thoroughly all assigned topics",
    backstory=(
        "You are an expert at navigating the internet to find the most "
        "relevant and up-to-date information. You have a knack for finding "
        "hidden gems and verifying the credibility of various web sources."
    ),
    # Use the tool instances created in section 3.1
    tools=[exa_search_tool, scrape_website_tool],
    verbose=True,
    max_iter=2,   # Load reduction: stop after 3 attempts to find info
    max_rpm=10,   # Load reduction: slow down requests to avoid 503 errors
    allow_delegation=False # Load reduction: don't let it start new sub-tasks
)

# Define the Fact Checker
fact_checker = Agent(
    role="Fact Checker",
    goal=(
        "Verify data for accuracy, identify inconsistencies, "
        "and flag potential misinformation"
    ),
    backstory=(
        "You are a meticulous analyst with a critical eye. You never take "
        "information at face value and always cross-reference data points "
        "to ensure the highest level of accuracy and reliability."
    ),
    # Fact checkers also need tools to verify claims online
    verbose=True,
    max_iter=2,   # Load reduction: stop after 3 attempts to find info
    max_rpm=10,   # Load reduction: slow down requests to avoid 503 errors
    allow_delegation=False # Load reduction: don't let it start new sub-tasks
)

# Define the Report Writer
report_writer = Agent(
    role="Report Writer",
    goal="Write clear, concise, and well-structured reports based on gathered information",
    backstory=(
        "You are a professional writer specialized in technical reporting. "
        "You can synthesize complex information into easy-to-understand "
        "executive summaries and detailed analytical sections."
    ),
    # The writer usually doesn't need search tools, just the info from the others
    tools=[], 
    verbose=True,
    max_iter=2,   # Load reduction: stop after 3 attempts to find info
    max_rpm=10,   # Load reduction: slow down requests to avoid 503 errors
    allow_delegation=False # Load reduction: don't let it start new sub-tasks
)



# <a id="4"></a>
# 
# ## 4. Create the Tasks
# 
# Now that you have set up the agents, it is time to define the tasks. If you go back to the diagram, you will see you need four tasks:
# 
# - **Create research plan**: Based on the user's query, break it down into specific topics and key questions, and create a focused research plan.
#     - Output: A research plan with main research topics to investigate, key questions for each topic, and success criteria for the research.
# 
# - **Gather research data**: Using the research plan, collect information on all identified topics. Cite all sources used.
#     - Output: Comprehensive research data including: information for each research topic, and citations used along with source credibility notes.
# 
# - **Verify information quality**: Review all collected research. Identify any conflicting information, potential misinformation, or gaps that need addressing.
#     - Output: A report with the all the collected data, and its review. It should include consistency check results and source reliability ratings
# 
# - **Write final report**: Create a comprehensive report that answers the original query using all verified research data. Structure it with clear sections, include citations, and provide actionable insights.
#     - Output: The final research report. In addition to the full answer, it should have an executive summary, and complete source citations.
# 
# 
# For each `Task` you need to define the following parameters:
# - `description`: A thorough description of the task. You can even break it down into different items.
# - `expected_output`: what should the output return. Be specific, specially if you want any structure in your result, like a dictionary with specific keys.
# - `agent`: who is performing the task? You need to match the task to one of the agents you already defined
# 
# In the description you will need to pass the inputs to the tasks. In this lab, you will only have as input the user's query, which will be saved as `user_query`:
# 
# 
# <a id="4-1"></a>
# 
# ### 4.1. Define the Create research plan task
# 
# In the cell below, you will see how you can create the first task. This time, all the parameters are set up for you. Notice how the context variables are passed the the description between curly brackets. 

# In[ ]:


# define the create research plan task
create_research_plan_task = Task(
    description=(
        "Based on the user's query, break it down into specific topics and key questions, "
        "and create a focused research plan."
        "The user's query is: {user_query}"
    ),
    expected_output=(
        "A research plan with main research topics to investigate, "
        "key questions for each topic, and success criteria for the research."
        ),
    agent=research_planner,
)


# <a id="4-2"></a>
# 
# ### 4.2. Define the remaining tasks
# 
# Now define the three remaining tasks. The `description` is already filled in for you, you will need to define the `expected_output` and `agent` for each of the Tasks.

# In[ ]:


# tasks_definition.py

# 4.2 Define the remaining tasks

# 1. Define the gather research data task
gather_research_data_task = Task(
    description=(
        "Using the research plan, collect information on all identified topics. "
        "Cite all sources used."
    ),
    ### START CODE HERE ###
    expected_output=(
        "Comprehensive research data including: information for each research topic, "
        "and citations used along with source credibility notes."
    ),
    agent=researcher # This matches the researcher agent created earlier
    ### END CODE HERE ###
)

# 2. Define the verify information quality task
verify_information_quality_task = Task(
    description=(
        "Review all collected research. Identify any conflicting information, "
        "potential misinformation, or gaps that need addressing."
    ),
    ### START CODE HERE ###
    expected_output=( 
        "A report with all the collected data and its review. "
        "It should include consistency check results and source reliability ratings."
    ),
    agent=fact_checker # This matches the fact_checker agent
    ### END CODE HERE ###
)

# 3. Define the write final report task
write_final_report_task = Task(
    description=(
        "Create a comprehensive report that answers the original query using all verified research data. "
        "Structure it with clear sections, include citations, and provide actionable insights."
    ),
    ### START CODE HERE ###
    expected_output=( 
        "The final research report. In addition to the full answer, it should have "
        "an executive summary and complete source citations."
    ),
    agent=report_writer # This matches the report_writer agent
    ### END CODE HERE ###
)


# <a id="5"></a>
# 
# ## 5. Define the Crew and get the results
# 
# Once the agents and tasks have been defined, you are ready to create the crew. In order to so, you will need to set the following arguments:
# - `agents`: list of agents in the crew
# - `tasks`: list of tasks in the crew. The tasks should be listed in the order they should be executed
# 
# In the next cell, fill in the agents and tasks for the crew.

# In[ ]:


# crew_setup.py

# create the crew with the defined agents and tasks
crew = Crew(
    ### START CODE HERE ###
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
    ### 
)


# Before running the crew, you need to define the query, which will be used as input for the tasks.

# In[ ]:


### START CODE HERE ###

# Write your query, which will be used as input for the tasks.
user_query = "The impact of generative AI on software engineering productivity in 2025"

### END CODE HERE ###


# Now you are only left with kickstarting the crew to get the results. Since you set `verbose=True` in the agents, you should monitor all the process.

# In[ ]:


# kickstart the crew to get the results
result = crew.kickoff(inputs={'user_query': user_query})


# From the output of the previous cell check all the outputs for each task. Do they match what you expected? If not, go back and refine the `expected_output`. 

# You can also print the final report to see the final result of the crew

# In[ ]:


# Display the final report
from IPython.display import Markdown
Markdown(result.raw)


# You made it to the end of the lab! You can go back and experiment with the goals and backstories of the agents, as well as description and expected outputs of tasks. You can also change the inputs to any research topic you wish. Have fun with it!
