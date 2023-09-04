from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import exc, select, ScalarResult

from lyceum_backend.db import tables
from lyceum_backend.schemas import group as group_schemas
from lyceum_backend.services.base import BaseService


class GroupService(BaseService):
    async def get_all(self) -> ScalarResult[tables.Group]:
        query = select(tables.Group)
        query = query.order_by(tables.Group.id)
        return await self.session.scalars(query)

    async def get(self, group_id: int | None = None) -> tables.Group | None:
        query = select(tables.Group)
        if group_id is not None:
            query = query.filter_by(id=group_id)
        group = await self.session.scalar(query)
        if group is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return group

    async def create(self, group_schema: group_schemas.GroupCreate) -> tables.Group:
        group = tables.Group(**group_schema.model_dump())
        self.session.add(group)
        await self.session.commit()
        self.response.status_code = status.HTTP_201_CREATED
        return group

    async def update(self, group_id: int, group_schema: group_schemas.GroupUpdate) -> tables.Group:
        query = select(tables.Group)
        query = query.filter_by(id=group_id)
        group = await self.session.scalar(query)
        if group is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        group.number = group_schema.number
        group.letter = group_schema.letter
        self.session.add(group)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return group

    async def delete(self, group_id: int):
        query = select(tables.Group)
        query = query.filter_by(id=group_id)
        group = await self.session.scalar(query)
        await self.session.delete(group)
        await self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
