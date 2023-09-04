import logging

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from lyceum_backend import schemas
from lyceum_backend.db.base import settings
from lyceum_backend.services.base import BaseService
from lyceum_backend.services.user import UserService

logger = logging.getLogger(__name__)

ALGORITHM = "HS256"


class AuthService(BaseService):
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.SESSION_LIFETIME
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="/api/login",
        scheme_name="oauth2_schema"
    )

    def __init__(self, user_service: UserService = Depends()):
        super().__init__()
        self.user_service = user_service

    async def create_user(self, user_schema: schemas.user.UserCreate):
        user_schema.password = self._get_password_hash(user_schema.password)
        return await self.user_service.create(user_schema)

    async def update_user(self, user_id: int, user_schema: schemas.user.UserUpdate):
        user_schema.password = self._get_password_hash(user_schema.password)
        return await self.user_service.update(user_id, user_schema)

    async def login(self, username: str, password: str) -> str:
        return "123456"

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password):
        return self.pwd_context.hash(password)

    @classmethod
    async def get_current_user(cls, token: str = Depends(oauth2_scheme)):
        return token
