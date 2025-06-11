from typing import Sequence

from cuid2 import cuid_wrapper

from .interfaces import I_ScheduleService
from .models import CreateSchedule, Schedule

_cuid_generator = cuid_wrapper()


class InMemoryScheduleService(I_ScheduleService):
    def __init__(self, store: dict[str, Schedule]):
        self._schedules = store

    def create_schedule(self, schedule: CreateSchedule) -> Schedule:
        new_schedule = Schedule(
            id=_cuid_generator(),
            title=schedule.title,
            start_at=schedule.start_at,
            end_at=schedule.end_at,
            category=schedule.category,
        )
        self._schedules[new_schedule.id] = new_schedule
        return new_schedule

    def list_schedules(self) -> Sequence[Schedule]:
        return list(self._schedules.values())

    def get_schedule_by_id(self, id_: str) -> Schedule:
        if schedule := self._schedules.get(id_):
            return schedule
        raise ValueError(f"Schedule with id {id_} does not exist.")

    def find_schedules_by_date(self, date: str) -> Sequence[Schedule]:
        return [
            schedule
            for schedule in self._schedules.values()
            if schedule.start_at.date().isoformat() == date
        ]

    def update_schedule(self, schedule: Schedule) -> Schedule:
        if schedule.id not in self._schedules:
            raise ValueError(f"Schedule with id {schedule.id} does not exist.")
        self._schedules[schedule.id] = schedule
        return schedule

    def delete_schedule(self, id_: str) -> Schedule:
        if id_ not in self._schedules:
            raise ValueError(f"Schedule with id {id_} does not exist.")
        return self._schedules.pop(id_)
