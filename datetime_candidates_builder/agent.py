from datetime import datetime
from typing import Literal
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel, Field

from llm_model import get_llm


class DatetimeSpan(BaseModel):
    """A span of time with a start and end datetime."""

    start_datetime: str = Field(
        description="The start date and time in ISO 8601 format (e.g., '2024-10-01T09:00:00+09:00').",
    )
    end_datetime: str = Field(
        description="The end date and time in ISO 8601 format (e.g., '2024-10-01T17:30:00+09:00').",
    )


class DatetimeCandidatesState(BaseModel):
    """A list of datetime spans representing candidates for a meeting."""

    candidates: list[DatetimeSpan]
    status: Literal["completed"] = "completed"


def get_current_time() -> dict:
    """Returns the current time.

    Returns:
        dict: status and result or error msg.
    """

    now = datetime.now(ZoneInfo("Asia/Tokyo"))
    report = f"The current time is {now.strftime('%Y-%m-%d (%A) %H:%M:%S %Z%z')}"
    return {"status": "success", "report": report}


save_state_agent = Agent(
    name="SaveDatetimeCandidates",
    model=get_llm(),
    description="`state['DatetimeCandidates']`に保存するデータ保存するエージェント。",
    instruction="受け取ったデータをそのまま出力してください。",
    output_key="DatetimeCandidates",
    output_schema=DatetimeCandidatesState,
)

root_agent = Agent(
    name="DatetimeCandidatesBuilder",
    model=get_llm(True),
    description=(
        """会議の候補日時(`DatetimeCandidates`)を特定するエージェント。
出力は`state['DatetimeCandidates']`に保存されます。"""
    ),
    instruction=(
        """「今日」や「今週」などのあいまいな表現や相対的な表現を、具体的な会議の候補日時へ変換してください。
ユーザーに聞き返す必要がある場合は、ユーザーの意図をくみ取って、できるだけクローズドクエスチョンで質問してください。

候補日時は日時指定です。
一般的に会議は日中に設定されるため、連続した複数日付が指示された場合も、日付ごとに分割して各日付の適切な時間帯を設定してください。

候補日時が特定できたら、`SaveDatetimeCandidates`ツールを使ってデータを保存してください。

ユーザーの確認が取れたら、親エージェントに転送してください。

## データ形式

### DatetimeCandidates

- candidates: `List[DatetimeSpan]`

### DatetimeSpan

- start: `datetime`
- end: `datetime`

## 参考情報

- 定時は9:00から17:30まで
- 平日は月曜日から金曜日
- 祝日は日本の祝日

## 例1

- ユーザー: 「今週の水曜日の午後3時から1時間」
- 現在日時: 2024-10-01(Tuesday) 10:00:00 JST
- 出力:
```json
{
  "candidates": [
    {
      "start": "2024-10-02T15:00:00+09:00",
      "end": "2024-10-02T16:00:00+09:00"
    }
  ]
}

## 例2

- ユーザー: 「今週のどこかで」
- 現在日時: 2024-10-01(Tuesday) 13:00:00 JST
- 出力:
```json
{
  "candidates": [
  {
      "start": "2024-10-01T15:00:00+09:00",
      "end": "2024-10-01T17:30:00+09:00"
    },
    {
      "start": "2024-10-02T09:00:00+09:00",
      "end": "2024-10-02T17:30:00+09:00"
    },
    {
      "start": "2024-10-03T09:00:00+09:00",
      "end": "2024-10-03T17:30:00+09:00"
    },
    {
      "start": "2024-10-04T09:00:00+09:00",
      "end": "2024-10-04T17:30:00+09:00"
    }
  ]
}

"""
    ),
    tools=[get_current_time, AgentTool(agent=save_state_agent)],
)
