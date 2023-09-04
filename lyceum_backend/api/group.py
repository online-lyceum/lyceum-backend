import logging

from fastapi import APIRouter, Depends

from lyceum_backend import schemas
from lyceum_backend.services.group import GroupService


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/groups',
    tags=["Groups"],
)


@router.get(
    '/',
    response_model=schemas.group.Group
)
async def get_groups(
        service: GroupService = Depends()
):
    return await service.get_all()


@router.get('/{group_id}', response_model=schemas.group.Group)
async def get_group(
        group_id: int,
        service: GroupService = Depends()
):
    return await service.get(group_id)


@router.post(
    '',
    response_model=schemas.group.Group
)
async def create_group(
        group_schema: schemas.group.GroupCreate,
        service: GroupService = Depends()
):
    return await service.create_group(group_schema)


@router.patch(
    '/{group_id}',
    response_model=schemas.group.Group
)
async def patch_group(
        group_id: int,
        group_schema: schemas.group.GroupUpdate,
        service: GroupService = Depends()
):
    return await service.update_group(group_id, group_schema)


@router.delete(
    '/{group_id}'
)
async def delete_group(
        group_id: int,
        service: GroupService = Depends()
):
    return await service.delete(group_id)
