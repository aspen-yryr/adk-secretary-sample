from typing import Annotated

from fastapi import APIRouter, Body, Depends, FastAPI

from schedule.dependencies import provide_schedule_service
from schedule.models import Schedule

from .interfaces import I_ScheduleService
from .schemas import (
    ScheduleCreateRequest,
    ScheduleListResponse,
    ScheduleResponse,
    ScheduleUpdateRequest,
)

sr = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
)


@sr.get("/")
def list_schedules(
    svc: Annotated[I_ScheduleService, Depends(provide_schedule_service)],
) -> ScheduleListResponse:
    """List all schedules."""
    schedules = svc.list_schedules()
    return ScheduleListResponse.of(schedules)


@sr.get("/")
def find_schedules_by_date(
    date: str,
    svc: Annotated[I_ScheduleService, Depends(provide_schedule_service)],
) -> ScheduleListResponse:
    return ScheduleListResponse.of(svc.find_schedules_by_date(date))


@sr.post("/")
def create_schedule(
    schedule: Annotated[ScheduleCreateRequest, Body()],
    svc: Annotated[I_ScheduleService, Depends(provide_schedule_service)],
) -> ScheduleResponse:
    return ScheduleResponse.of(svc.create_schedule(schedule.to_model()))


@sr.get("/{id_}")
def get_schedule_by_id(
    id_: str,
    svc: Annotated[I_ScheduleService, Depends(provide_schedule_service)],
) -> ScheduleResponse:
    return ScheduleResponse.of(svc.get_schedule_by_id(id_))


@sr.put("/{id_}")
def update_schedule(
    id_: str,
    schedule: Annotated[ScheduleUpdateRequest, Body()],
    svc: Annotated[I_ScheduleService, Depends(provide_schedule_service)],
) -> ScheduleResponse:
    # TODO
    if id_ != schedule.id:
        raise ValueError("ID in path and body must match.")

    return ScheduleResponse.of(
        svc.update_schedule(
            Schedule(
                id=id_,
                title=schedule.title,
                start_at=schedule.start_at,
                end_at=schedule.end_at,
                category=schedule.category,
            )
        )
    )


@sr.delete("/{id_}")
def delete_schedule(
    id_: str,
    svc: Annotated[I_ScheduleService, Depends(provide_schedule_service)],
) -> ScheduleResponse:
    return ScheduleResponse.of(svc.delete_schedule(id_))


app = FastAPI(
    description="""Schedule API
This API allows you to manage schedules, including creating, listing, updating, and retrieving schedules by date or ID.""",
    servers=[
        {
            "url": "http://localhost:8005",
            "description": "Schedule API",
        }
    ],
)

base_router = APIRouter(prefix="/api/v1")
base_router.include_router(sr)

app.include_router(base_router)
