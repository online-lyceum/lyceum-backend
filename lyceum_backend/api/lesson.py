import datetime as dt
import logging

from fastapi import APIRouter, Depends

from lyceum_backend import schemas
from lyceum_backend.services.lesson import LessonService

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/lessons',
    tags=["Lessons"],
)


@router.get(
    '/pack/{date}',
    response_model=list[schemas.lesson.Lesson],
    description="Return current day lessons and additional 7 days before and "
                "after"
)
async def get_lessons(
        date: dt.date,
        group_id: int | None = None,
        subgroup_id: int | None = None,
        service: LessonService = Depends()
):
    return await service.get_pack(date, group_id, subgroup_id)


@router.get(
    '/{date}', response_model=list[schemas.lesson.Lesson],
    description="Return current day lessons"
)
async def get_lesson(
        date: dt.date,
        group_id: int | None = None,
        subgroup_id: int | None = None,
        service: LessonService = Depends()
):
    return await service.get_day(date, group_id, subgroup_id)


@router.post(
    '',
    response_model=schemas.lesson.Lesson
)
async def create_lesson(
        lesson_schema: schemas.lesson.LessonCreate,
        service: LessonService = Depends()
):
    return await service.create(lesson_schema)


@router.patch(
    '/{lesson_id}',
    response_model=schemas.lesson.Lesson
)
async def patch_lesson(
        lesson_id: int,
        lesson_schema: schemas.lesson.LessonUpdate,
        service: LessonService = Depends()
):
    return await service.update(lesson_id, lesson_schema)


@router.delete(
    '/{lesson_id}'
)
async def delete_lesson(
        lesson_id: int,
        service: LessonService = Depends()
):
    return await service.delete(lesson_id)


@router.post(
    '/{lesson_id}/subgroup/{subgroup_id}'
)
async def add_subgroup_to_lesson(
        lesson_id: int,
        subgroup_id: int,
        service: LessonService = Depends()
):
    return await service.add_subgroup(lesson_id, subgroup_id)


@router.delete(
    '/{lesson_id}/subgroup/{subgroup_id}'
)
async def add_subgroup_to_lesson(
        lesson_id: int,
        subgroup_id: int,
        service: LessonService = Depends()
):
    return await service.delete_subgroup(lesson_id, subgroup_id)
