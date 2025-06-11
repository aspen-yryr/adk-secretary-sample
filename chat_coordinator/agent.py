import litellm
from google.adk.agents import Agent

from datetime_candidates_builder.agent import root_agent as time_condition_builder_agent
from llm_model import get_llm
from participants_condition_builder.agent import (
    root_agent as participants_condition_builder_agent,
)
from schedule_manager.agent import root_agent as schedule_manager_agent

litellm.suppress_debug_info = False

root_agent = Agent(
    name="ChatMeetingScheduleCoordinator",
    model=get_llm(True),
    description=("会議の日程調整をサポートします。全体的な制御を行います。"),
    instruction=(
        """ユーザーの会議の日程調整をサポートしてください。

候補日に関しては`DatetimeCandidatesBuilder`エージェントに、
参加者に関しては`ParticipantsConditionBuilder`エージェントに、
スケジュールの読み書きに関しては`ScheduleManager`エージェントに転送してください。

stateに、候補日と参加者の情報が保存されたら、ユーザーに確認を取ってからスケジュールを保存してください。
"""
    ),
    sub_agents=[
        participants_condition_builder_agent,
        time_condition_builder_agent,
        schedule_manager_agent,
    ],
)
