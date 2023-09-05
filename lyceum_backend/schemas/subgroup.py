from pydantic import BaseModel


class SubgroupBase(BaseModel):
    name: str = ""
    group_id: int

    class Config:
        from_attributes = True


class SubgroupCreate(SubgroupBase):
    pass


class Subgroup(SubgroupBase):
    pass


class SubgroupUpdate(BaseModel):
    name: str | None = None
    group_id: int | None = None

    class Config:
        from_attributes = True
