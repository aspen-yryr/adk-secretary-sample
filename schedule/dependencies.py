from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from schedule.models import Schedule

from .interfaces import I_ScheduleService


@lru_cache
def provide_schedule_store() -> dict[str, Schedule]:
    """Provides an in-memory store for schedules."""
    return {}


def provide_schedule_service(
    store: Annotated[dict[str, Schedule], Depends(provide_schedule_store)],
) -> I_ScheduleService:
    from schedule.services import InMemoryScheduleService

    return InMemoryScheduleService(store)
