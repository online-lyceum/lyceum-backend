from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import exc, ScalarResult, select

from lyceum_backend.db import tables
from lyceum_backend.schemas import school as school_schemas
from lyceum_backend.services.base import BaseService


class SchoolService(BaseService):
    async def get_all(self) -> ScalarResult[tables.School]:
        query = select(tables.School)
        query = query.order_by(tables.School.id)
        return await self.session.scalars(query)

    async def get(self, school_id: int | None = None) -> tables.School | None:
        query = select(tables.School)
        if school_id is not None:
            query = query.filter_by(id=school_id)
        school = await self.session.scalar(query)
        if school is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return school

    async def create(
            self,
            school_schema: school_schemas.SchoolCreate
            ) -> tables.School:
        school = tables.School(**school_schema.model_dump())
        self.session.add(school)
        await self.session.commit()
        self.response.status_code = status.HTTP_201_CREATED
        return school

    async def update(
            self,
            school_id: int,
            school_schema: school_schemas.SchoolUpdate
            ) -> tables.School:
        query = select(tables.School)
        query = query.filter_by(id=school_id)
        school = await self.session.scalar(query)
        if school is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        school.name = school_schema.name
        school.address = school_schema.address
        self.session.add(school)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return school

    async def delete(self, school_id: int):
        query = select(tables.School)
        query = query.filter_by(id=school_id)
        school = await self.session.scalar(query)
        await self.session.delete(school)
        await self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
