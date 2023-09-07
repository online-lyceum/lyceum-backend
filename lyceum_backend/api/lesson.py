import datetime as dt
import json
import logging

from fastapi import APIRouter, Depends

from lyceum_backend import schemas
from lyceum_backend.services.lesson import LessonService

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/lessons',
    tags=["Lessons"],
)


def lesson_model_to_lesson(lesson_model):
    return schemas.lesson.Lesson(
        id=lesson_model.id,
        name=lesson_model.name,
        room=lesson_model.room,
        teacher=lesson_model.teacher,
        start_dt=lesson_model.start_dt,
        end_dt=lesson_model.end_dt,
        breaks=json.loads(lesson_model.breaks)
    )


def lesson_models_to_lessons(lesson_models):
    return [lesson_model_to_lesson(model) for model in lesson_models]


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
    lesson_models = await service.get_pack(date, group_id, subgroup_id)
    return lesson_models_to_lessons(lesson_models)


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
    lesson_models = await service.get_day(date, group_id, subgroup_id)
    return lesson_models_to_lessons(lesson_models)


def dump_breaks(breaks: list[schemas.lesson.Break]) -> str:
    return json.dumps(
        [{
            'start_dt': break_time.start_dt.isoformat(),
            'end_dt': break_time.end_dt.isoformat()
        } for break_time in breaks]
    )


@router.post(
    '',
    response_model=schemas.lesson.Lesson
)
async def create_lesson(
        lesson_schema: schemas.lesson.LessonCreate,
        service: LessonService = Depends()
):
    inside_lesson_schema = schemas.lesson.InsideLessonCreate(
        **lesson_schema.model_dump(exclude={'breaks'}),
        breaks=dump_breaks(lesson_schema.breaks)
    )
    lesson_model = await service.create(inside_lesson_schema)
    return lesson_models_to_lessons([lesson_model])[0]


@router.patch(
    '/{lesson_id}',
    response_model=schemas.lesson.Lesson
)
async def patch_lesson(
        lesson_id: int,
        lesson_schema: schemas.lesson.LessonUpdate,
        service: LessonService = Depends()
):
    lesson_model = await service.update(lesson_id, lesson_schema)
    return lesson_models_to_lessons([lesson_model])[0]


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
