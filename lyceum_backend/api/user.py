import logging

from fastapi import APIRouter, Depends, HTTPException, status

from lyceum_backend import schemas
from lyceum_backend.db import tables
from lyceum_backend.services.auth import AuthService, current_user
from lyceum_backend.services.user import UserService

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/users',
    tags=["Users"],
)


@router.get(
    '/me',
    response_model=schemas.user.User
)
async def get_user(
        user: tables.User = Depends(current_user)
):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


@router.post(
    '',
    response_model=schemas.user.User
)
async def create_user(
        user_schema: schemas.user.UserCreate,
        service: AuthService = Depends()
):
    return await service.create_user(user_schema)


@router.patch(
    '/me',
    response_model=schemas.user.User
)
async def patch_user(
        user_schema: schemas.user.UserUpdate,
        service: AuthService = Depends(),
        user: tables.User = Depends(current_user)
):
    return await service.update_user(user.id, user_schema)


@router.delete(
    '/me'
)
async def delete_user(
        service: UserService = Depends(),
        user: tables.User = Depends(current_user)
):
    return await service.delete(user.id)
