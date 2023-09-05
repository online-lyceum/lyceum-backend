from pydantic import BaseModel


class GroupBase(BaseModel):
    letter: str | None = None
    number: int | None = None
    school_id: int

    class Config:
        from_attributes = True


class GroupCreate(GroupBase):
    pass


class Group(GroupBase):
    id: int


class GroupUpdate(BaseModel):
    letter: str | None = None
    number: int | None = None
    school_id: int | None = None

    class Config:
        from_attributes = True
