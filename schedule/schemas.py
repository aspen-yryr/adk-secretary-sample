from datetime import datetime
from typing import Literal, Sequence

from pydantic import BaseModel, ConfigDict, Field

from .models import CreateSchedule, Schedule


class _Schedule(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    title: str
    start_at: datetime
    end_at: datetime
    category: Literal["present", "meeting", "rest", "other"]


class ScheduleCreateRequest(_Schedule):
    def to_model(self) -> CreateSchedule:
        return CreateSchedule(
            title=self.title,
            start_at=self.start_at,
            end_at=self.end_at,
            category=self.category,
        )


class ScheduleUpdateRequest(_Schedule):
    id: str

    def to_model(self) -> Schedule:
        return Schedule(
            id=self.id,
            title=self.title,
            start_at=self.start_at,
            end_at=self.end_at,
            category=self.category,
        )


class ScheduleResponse(_Schedule):
    id: str

    @classmethod
    def of(cls, schedule: Schedule) -> "ScheduleResponse":
        return cls(
            id=schedule.id,
            title=schedule.title,
            start_at=schedule.start_at,
            end_at=schedule.end_at,
            category=schedule.category,
        )


class ScheduleListResponse(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schedules: Sequence[ScheduleResponse] = Field(
        default_factory=list, description="List of schedules"
    )
    total: int = Field(default=0, description="Total number of schedules")

    @classmethod
    def of(cls, schedules: Sequence[Schedule]) -> "ScheduleListResponse":
        return cls(
            schedules=[ScheduleResponse.of(s) for s in schedules],
            total=len(schedules),
        )
