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
    breaks: list[Break]

    class Config:
        from_attributes = True


class LessonCreate(LessonBase):
    pass


class Lesson(LessonBase):
    id: int


class LessonUpdate(BaseModel):
    name: str | None = None
    start_dt: dt.datetime | None = None
    end_dt: dt.datetime | None = None
    room: int | None = None
    teacher: str | None = None
    breaks: list[Break] | None = None

    class Config:
        from_attributes = True
