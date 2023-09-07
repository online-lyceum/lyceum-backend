import datetime as dt

from pydantic import BaseModel


class Break(BaseModel):
    start_dt: dt.datetime
    end_dt: dt.datetime


class LessonBase(BaseModel):
    name: str
    room: str
    teacher: str
    start_dt: dt.datetime
    end_dt: dt.datetime

    class Config:
        from_attributes = True


class LessonCreate(LessonBase):
    breaks: list[Break]


class InsideLessonCreate(LessonBase):
    breaks: str = "[]"

    class Config:
        from_attributes = True


class Lesson(LessonBase):
    id: int
    breaks: list[Break]


class LessonUpdate(BaseModel):
    name: str | None = None
    start_dt: dt.datetime | None = None
    end_dt: dt.datetime | None = None
    room: int | None = None
    teacher: str | None = None
    breaks: list[Break] | None = None

    class Config:
        from_attributes = True
