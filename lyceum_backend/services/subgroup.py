from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import exc, select, ScalarResult

from lyceum_backend.db import tables
from lyceum_backend.schemas import subgroup as subgroup_schemas
from lyceum_backend.services.base import BaseService


class SubgroupService(BaseService):
    async def get_all(self) -> ScalarResult[tables.Subgroup]:
        query = select(tables.Subgroup)
        query = query.order_by(tables.Subgroup.id)
        return await self.session.scalars(query)

    async def get(self, subgroup_id: int | None = None) -> tables.Subgroup | None:
        query = select(tables.Subgroup)
        if subgroup_id is not None:
            query = query.filter_by(id=subgroup_id)
        subgroup = await self.session.scalar(query)
        if subgroup is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return subgroup

    async def create(self, subgroup_schema: subgroup_schemas.SubgroupCreate) -> tables.Subgroup:
        subgroup = tables.Subgroup(**subgroup_schema.model_dump())
        self.session.add(subgroup)
        await self.session.commit()
        self.response.status_code = status.HTTP_201_CREATED
        return subgroup

    async def update(self, subgroup_id: int, subgroup_schema: subgroup_schemas.SubgroupUpdate) -> tables.Subgroup:
        query = select(tables.Subgroup)
        query = query.filter_by(id=subgroup_id)
        subgroup = await self.session.scalar(query)
        if subgroup is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        subgroup.name = subgroup_schema.name
        self.session.add(subgroup)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return subgroup

    async def delete(self, subgroup_id: int):
        query = select(tables.Subgroup)
        query = query.filter_by(id=subgroup_id)
        subgroup = await self.session.scalar(query)
        await self.session.delete(subgroup)
        await self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
