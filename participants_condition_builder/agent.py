from typing import Literal

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel

from llm_model import get_llm


class ParticipantsConditionState(BaseModel):
    """A list of datetime spans representing candidates for a meeting."""

    participant_names: list[str]
    status: Literal["completed"] = "completed"


save_state_agent = Agent(
    name="SaveParticipantsCondition",
    model=get_llm(),
    description="`state['MeetingParticipants']`に保存するデータ保存するエージェント。",
    instruction="受け取ったデータをそのまま出力してください。",
    output_key="MeetingParticipants",
    output_schema=ParticipantsConditionState,
)

root_agent = Agent(
    name="ParticipantsConditionBuilder",
    model=get_llm(),
    description=(
        """会議の参加者(`MeetingParticipants`)を特定するエージェント
出力は`state['MeetingParticipants']`に保存されます。"""
    ),
    instruction=(
        """会議の参加者を特定してください。
曖昧な名前が含まれたり参加者を特定するのが難しい場合は、ユーザーに具体的な名前を確認してください。

参加者が特定できたら、`SaveParticipantsCondition`ツールを使って以下のデータを保存してください。

参加者についてユーザーの確認が取れたら、親エージェントに転送してください。

## MeetingParticipants

- participants: `List[Participant]`

## Participant

- name: `str`
"""
    ),
    tools=[AgentTool(agent=save_state_agent)],
)
