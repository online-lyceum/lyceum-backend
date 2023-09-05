from fastapi import status
from fastapi.exceptions import HTTPException
from sqlalchemy import exc, select

from lyceum_backend.db import tables
from lyceum_backend.schemas import user as user_schemas
from lyceum_backend.services.base import BaseService


class UserService(BaseService):
    async def get_list(self):
        query = select(tables.User)
        query = query.order_by(tables.User.id)
        return await self.session.scalars(query)

    async def get(
            self, user_id: int | None = None, username: str | None = None,
            raise_exception: bool = True
            ) -> tables.User | None:
        query = select(tables.User)
        if user_id is not None:
            query = query.filter_by(id=user_id)
        if username is not None:
            query = query.filter_by(username=username)
        user = await self.session.scalar(query)
        if user is None:
            if not raise_exception:
                return
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    async def create(self, user_schema: user_schemas.UserCreate) -> tables.User:
        user = tables.User(**user_schema.model_dump())
        self.session.add(user)
        await self.session.commit()
        self.response.status_code = status.HTTP_201_CREATED
        return user

    async def update(
            self,
            user_id: int,
            user_schema: user_schemas.UserUpdate
            ) -> tables.User:
        query = select(tables.User)
        query = query.filter_by(id=user_id)
        user = await self.session.scalar(query)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        user.username = user_schema.username or user.username
        user.first_name = user_schema.first_name or user.first_name
        user.last_name = user_schema.last_name or user.last_name
        user.subgroup_id = user_schema.subgroup_id or user.subgroup_id
        user.password = user_schema.password or user.password
        self.session.add(user)
        try:
            await self.session.commit()
        except exc.IntegrityError:
            await self.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return user

    async def delete(self, user_id: int):
        query = select(tables.User)
        query = query.filter_by(id=user_id)
        user = await self.session.scalar(query)
        await self.session.delete(user)
        await self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
