from typing import List

from crewai import Agent, Crew, LLM, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os

_env = {}

def create_llm():
    env = _env
    api_key = (
        env.get("AI_GATEWAY_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    )
    base_url = (
        env.get("AI_GATEWAY_BASE_URL")
        or os.environ.get("OPENAI_API_BASE")
        or ""
    )
    model_id = (
        env.get("AI_GATEWAY_MODEL")
        or os.environ.get("OPENAI_MODEL_NAME")
        or "gpt-4o"
    )

    if not api_key:
        raise RuntimeError(
            "Missing AI_GATEWAY_API_KEY. "
            "Please set AI_GATEWAY_API_KEY in the EdgeOne Makers console environment variables. "
            "This is required for the LLM provider."
        )

    if model_id.startswith("openai/"):
        model_id = model_id[len("openai/"):]
    model = f"openai/{model_id}"
    kwargs = {
        "model": model,
        "api_key": api_key,
        "temperature": 0.1,
    }
    if base_url:
        kwargs["base_url"] = base_url

    return LLM(**kwargs)


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
            llm=create_llm(),
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],  # type: ignore[index]
        )

    @task
    def research_task_cn(self) -> Task:
        return Task(
            config=self.tasks_config["research_task_cn"],  # type: ignore[index]
            context=[self.research_task()],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
