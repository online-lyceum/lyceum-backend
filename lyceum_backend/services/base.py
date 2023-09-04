from fastapi import Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from lyceum_backend.db.base import get_session


class BaseService:
    def __init__(
            self,
            session=Depends(get_session),
            response: Response = Response
    ):
        self.session: AsyncSession = session
        self.response = response
