from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class CreateSchedule(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    title: str
    start_at: datetime
    end_at: datetime
    category: Literal["present", "meeting", "rest", "other"]

    def __str__(self):
        return f"CreateSchedule(title={self.title}, start_at={self.start_at}, end_at={self.end_at}, category={self.category})"


class Schedule(CreateSchedule):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: str

    def __str__(self):
        return f"Schedule(id={self.id}, title={self.title}, start_at={self.start_at}, end_at={self.end_at}, category={self.category})"
