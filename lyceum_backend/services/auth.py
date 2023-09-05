import datetime as dt
import logging
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select

from lyceum_backend import schemas
from lyceum_backend.db import tables
from lyceum_backend.db.base import settings
from lyceum_backend.services.base import BaseService
from lyceum_backend.services.user import UserService

logger = logging.getLogger(__name__)

ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/login",
    scheme_name="oauth2_schema"
)


class AuthService(BaseService):
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.SESSION_LIFETIME
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def user_service(self):
        return UserService(self.session, self.response)

    async def create_user(self, user_schema: schemas.user.UserCreate):
        user_schema.password = self._get_password_hash(user_schema.password)
        return await self.user_service().create(user_schema)

    async def update_user(
            self,
            user_id: int,
            user_schema: schemas.user.UserUpdate
            ):
        user_schema.password = self._get_password_hash(user_schema.password)
        return await self.user_service().update(user_id, user_schema)

    async def login(self, username: str, password: str) -> str:
        token = str(uuid.uuid4())
        user = await self._auth(username, password)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        self.redis.set(token, user.id)
        self.redis.expire(
            token, dt.timedelta(
                minutes=int(self.ACCESS_TOKEN_EXPIRE_MINUTES)
                )
            )
        return token

    async def _auth(self, username: str, password: str) -> tables.User | None:
        query = select(tables.User).filter_by(username=username)
        user = await self.session.scalar(query)
        if user is None or not self._verify_password(password, user.password):
            return None
        return user

    def _verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password):
        return self.pwd_context.hash(password)

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        return await self._get_current_user(token)

    async def _get_current_user(self, token: str):
        user_id = int(self.redis.get(token))
        query = select(tables.User).filter_by(id=user_id)
        user = await self.session.scalar(query)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user

    @classmethod
    async def admin(cls, token: str = Depends(oauth2_scheme)):
        user = await cls()._get_current_user(token)
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        return user


async def current_user(
        service: AuthService = Depends(),
        token: str = Depends(oauth2_scheme)
        ):
    return await service.get_current_user(token)


async def admin(
        service: AuthService = Depends(),
        token: str = Depends(oauth2_scheme)
        ):
    return await service.admin(token)
