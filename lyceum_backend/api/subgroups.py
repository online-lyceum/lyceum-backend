import logging

from fastapi import APIRouter, Depends, HTTPException, status

from lyceum_backend import schemas
from lyceum_backend.db import tables
from lyceum_backend.services.auth import AuthService
from lyceum_backend.services.subgroup import SubgroupService


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/subgroups',
    tags=["Subgroups"],
)


@router.get(
    '/',
    response_model=schemas.subgroups.Subgroup
)
async def get_subgroups(
        service: SubgroupService = Depends()
):
    return await service.get_all()


@router.subgroup(
    '',
    response_model=schemas.subgroups.Subgroup
)
async def create_subgroup(
        subgroup_schema: schemas.subgroup.SubgroupCreate,
        service: AuthService = Depends()
):
    return await service.create_subgroup(subgroup_schema)


@router.patch(
    '/{subgroup_id}',
    response_model=schemas.subgroups.Subgroup
)
async def patch_subgroup(
        subgroup_id: int,
        subgroup_schema: schemas.subgroups.SubgroupUpdate,
        service: AuthService = Depends()
):
    return await service.update_subgroup(subgroup_id, subgroup_schema)


@router.delete(
    '/{subgroup_id}'
)
async def delete_subgroup(
        subgroup_id: int,
        service: SubgroupService = Depends()
):
    return await service.delete(subgroup_id)
