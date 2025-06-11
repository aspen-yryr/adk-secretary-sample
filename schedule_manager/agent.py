from google.adk.agents import Agent

from llm_model import get_llm

from .openapi import toolset

root_agent = Agent(
    name="ScheduleManager",
    model=get_llm(),
    description=("スケジュールのCRUDを行うエージェント"),
    tools=[toolset],
)
