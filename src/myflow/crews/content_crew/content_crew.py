# src/latest_ai_flow/crews/content_crew/content_crew.py
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
# from langchain_ollama import OllamaLLM
from crewai import LLM
import os
import dotenv

dotenv.load_dotenv(dotenv_path="../../")




llm  = LLM(
  model=os.getenv("MODEL"),
  base_url=os.getenv("BASE_URL"),
  api_key=os.getenv("API_KEY"),
  temperature=0.1
)




@CrewBase
class ResearchCrew:
  """Single-agent research crew used inside the Flow."""

  agents: List[BaseAgent]
  tasks: List[Task]

  agents_config = "config/agents.yaml"
  tasks_config = "config/tasks.yaml"

  @agent
  def researcher(self) -> Agent:
    return Agent(
      config=self.agents_config["researcher"],  # type: ignore[index]
      verbose=True,
      tools=[SerperDevTool()],
      llm=llm
    )

  @task
  def research_task(self) -> Task:
    return Task(
      config=self.tasks_config["research_task"],  # type: ignore[index]
    )
  
  @task
  def research_task_cn(self) -> Task:
    return Task(
      config=self.tasks_config["research_task_cn"],
    )

  @crew
  def crew(self) -> Crew:
    return Crew(
      agents=self.agents,
      tasks=self.tasks,
      process=Process.sequential,
      verbose=True,
    )