from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from crewai import LLM
import os


def create_llm():
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_API_BASE", "")
    model = os.environ.get("OPENAI_MODEL_NAME", "openai/gpt-4o")

    llm_kwargs = {
        "model": model,
        "temperature": 0.1,
    }
    if base_url:
        llm_kwargs["base_url"] = base_url
    if api_key:
        llm_kwargs["api_key"] = api_key

    return LLM(**llm_kwargs)


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
      llm=create_llm()
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
