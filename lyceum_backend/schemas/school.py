from pydantic import BaseModel


class SchoolBase(BaseModel):
    name: str
    address: str = ""

    class Config:
        from_attributes = True


class SchoolCreate(SchoolBase):
    pass


class School(SchoolBase):
    id: int


class SchoolUpdate(BaseModel):
    name: str | None = None
    address: str = ""
    group_id: int | None = None

    class Config:
        from_attributes = True
