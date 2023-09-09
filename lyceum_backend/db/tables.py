from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy import UniqueConstraint

from lyceum_backend.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    subgroup_id = Column(ForeignKey('subgroups.id'), nullable=True)
    is_admin = Column(Boolean, nullable=False, default=False)


class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, default="")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    school_id = Column(
        ForeignKey('schools.id', ondelete='CASCADE'), nullable=False
    )
    number = Column(Integer)
    letter = Column(String)

    __table_args__ = (
        UniqueConstraint('school_id', 'number', 'letter'),
    )


class Subgroup(Base):
    __tablename__ = 'subgroups'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, default="")
    group_id = Column(
        ForeignKey('groups.id', ondelete='CASCADE'), nullable=False
    )


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_dt = Column(DateTime, nullable=False)
    end_dt = Column(DateTime, nullable=False)
    room = Column(String, default='')
    teacher = Column(String, default='')
    breaks = Column(String, default='[]', nullable=False)


class LessonSubgroup(Base):
    __tablename__ = "lesson_subgroups"
    lesson_id = Column(
        ForeignKey('lessons.id', ondelete='CASCADE'), nullable=False,
        primary_key=True
    )
    subgroup_id = Column(
        ForeignKey('subgroups.id', ondelete='CASCADE'), nullable=False,
        primary_key=True
    )
