import datetime as dt

from pydantic import BaseModel


class LessonBase(BaseModel):
    name: str
    start_dt: dt.datetime
    end_dt: dt.datetime
    room: str
    teacher: str

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

    class Config:
        from_attributes = True
