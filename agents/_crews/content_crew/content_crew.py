from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai import LLM
import os

MODEL = os.environ.get("MODEL", "openai/gpt-4o")
BASE_URL = os.environ.get("BASE_URL", "")
API_KEY = os.environ.get("API_KEY", "")

llm_kwargs = {
    "model": MODEL,
    "temperature": 0.1,
}
if BASE_URL:
    llm_kwargs["base_url"] = BASE_URL
if API_KEY:
    llm_kwargs["api_key"] = API_KEY

llm = LLM(**llm_kwargs)


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
      config=self.agents_config["researcher"],
      verbose=True,
      tools=[SerperDevTool()],
      llm=llm
    )

  @task
  def research_task(self) -> Task:
    return Task(
      config=self.tasks_config["research_task"],
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
