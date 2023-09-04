from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from lyceum_backend.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    subgroup_id = Column(ForeignKey('subgroups.id'), nullable=True)


class School(Base):
    __tablename__ = "schools"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    school_id = Column(ForeignKey('schools.id'))
    number = Column(Integer)
    letter = Column(String)


class Subgroup(Base):
    __tablename__ = 'subgroups'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, nullable=False)
    start_dt = Column(DateTime, nullable=False)
    end_dt = Column(DateTime, nullable=False)
    room = Column(String, server_default='')
    teacher = Column(String, server_default='')


class LessonSubgroup(Base):
    __tablename__ = "lesson_subgroups"
    lesson_id = Column(ForeignKey('lessons.id'), nullable=False, primary_key=True)
    subgroup_id = Column(ForeignKey('subgroups.id'), nullable=False, primary_key=True)
