import datetime as dt

from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import exc, ScalarResult, select

from lyceum_backend.db import tables
from lyceum_backend.schemas import lesson as lesson_schemas
from lyceum_backend.services.base import BaseService


class LessonService(BaseService):
    async def get_day(
            self,
            day: dt.date,
            group_id: int | None = None,
            subgroup_id: int | None = None
    ) -> ScalarResult[tables.Lesson]:
        if group_id is None and subgroup_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        query = select(tables.Lesson)
        query = query.filter(
            tables.Lesson.start_dt > day.isoformat()
        )
        query = query.filter(
            tables.Lesson.end_dt < dt.datetime.fromisoformat(
                day.isoformat()
            ) + dt.timedelta(days=1)
        )
        query = query.join(tables.LessonSubgroup)
        if subgroup_id is not None:
            query = query.filter(tables.Subgroup.id == subgroup_id)
        if group_id is not None:
            query = query.join(tables.Subgroup)
            query = query.filter_by(group_id=group_id)
        query = query.order_by(tables.Lesson.start_dt)
        return await self.session.scalars(query)

    async def get_pack(
            self,
            day: dt.date,
            group_id: int | None = None,
            subgroup_id: int | None = None
    ) -> ScalarResult[tables.Lesson]:
        if group_id is None and subgroup_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        query = select(tables.Lesson)
        query = query.filter(
            tables.Lesson.start_dt > (dt.datetime.fromisoformat(
                day.isoformat()
            ) - dt.timedelta(days=7))
        )
        query = query.filter(
            tables.Lesson.end_dt < dt.datetime.fromisoformat(
                day.isoformat()
            ) + dt.timedelta(days=7)
        )
        query = query.join(tables.LessonSubgroup)
        if subgroup_id is not None:
            query = query.filter(tables.Subgroup.id == subgroup_id)
        if group_id is not None:
            query = query.join(tables.Subgroup)
            query = query.filter_by(group_id=group_id)
        query = query.order_by(tables.Lesson.start_dt)
        return await self.session.scalars(query)

    async def create(
            self,
            lesson_schema: lesson_schemas.LessonCreate
    ) -> tables.Lesson:
        lesson = tables.Lesson(
            **lesson_schema.model_dump(exclude={'start_dt', 'end_dt', 'breaks'})
        )
        lesson.start_dt = self._normalize_time(lesson_schema.start_dt)
        lesson.end_dt = self._normalize_time(lesson_schema.end_dt)
        self.session.add(lesson)
        for break_time in lesson_schema.breaks:
            self.session.add(
                tables.Break(
                    start_dt=self._normalize_time(break_time.start_dt),
                    end_dt=self._normalize_time(break_time.end_dt)
                )
            )
        await self.session.commit()
        self.response.status_code = status.HTTP_201_CREATED
        return lesson

    async def _normalize_time(self, datetime: dt.datetime):
        return datetime.replace(tzinfo=None)

    async def update(
            self,
            lesson_id: int,
            lesson_schema: lesson_schemas.LessonUpdate
    ) -> tables.Lesson:
        query = select(tables.Lesson)
        query = query.filter_by(id=lesson_id)
        lesson = await self.session.scalar(query)
        if lesson is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        lesson_schema: dict = lesson_schema.model_dump()
        for attr in lesson_schema.keys():
            setattr(lesson, attr, lesson_schema[attr])
        self.session.add(lesson)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return lesson

    async def delete(self, lesson_id: int):
        query = select(tables.Lesson)
        query = query.filter_by(id=lesson_id)
        lesson = await self.session.scalar(query)
        await self.session.delete(lesson)
        await self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT

    async def add_subgroup(self, lesson_id: int, subgroup_id: int):
        lesson_subgroup = tables.LessonSubgroup(
            lesson_id=lesson_id, subgroup_id=subgroup_id
        )
        self.session.add(lesson_subgroup)
        await self.session.commit()
        return lesson_subgroup

    async def delete_subgroup(self, lesson_id: int, subgroup_id: int):
        query = select(tables.LessonSubgroup).filter_by(
            lesson_id=lesson_id, subgroup_id=subgroup_id
        )
        lesson_subgroup = await self.session.scalar(query)
        await self.session.delete(lesson_subgroup)
        await self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
