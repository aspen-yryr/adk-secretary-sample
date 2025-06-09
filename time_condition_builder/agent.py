from google.adk.agents import Agent

from google.adk.models.lite_llm import LiteLlm
from datetime import datetime

from config import config


def get_current_time() -> dict:
    """Returns the current time.

    Returns:
        dict: status and result or error msg.
    """

    # tz = ZoneInfo(tz_identifier)
    now = datetime.now()
    report = f"The current time is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    return {"status": "success", "report": report}


root_agent = Agent(
    name="datetime_condition_builder",
    model=LiteLlm(
        model="openai/gpt-4o-2024-08-06",
        api_key=config.api_key.get_secret_value(),
    ),
    description=(
        "ユーザーとチャットで対話して、会議の日程条件(`DatetimeCondition`)を決定するエージェント"
    ),
    instruction=(
        """ユーザーとチャットで対話して、`DatetimeCondition`を洗い出してください。
会議の日程条件(`DatetimeCondition`)をすべて聞き取ったら、ユーザーに確認のメッセージを送信してください。

## DatetimeCondition

- datetime_spans: `List[DatetimeSpan]`

## DatetimeSpan

- start: `datetime`
- end: `datetime`

"""
    ),
    tools=[get_current_time],
)
