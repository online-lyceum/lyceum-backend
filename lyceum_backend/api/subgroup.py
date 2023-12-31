import logging

from fastapi import APIRouter, Depends

from lyceum_backend import schemas
from lyceum_backend.services.subgroup import SubgroupService

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/subgroups',
    tags=["Subgroups"],
)


@router.get(
    '',
    response_model=list[schemas.subgroup.Subgroup]
)
async def get_subgroups(
        school_id: int | None = None,
        service: SubgroupService = Depends()
):
    return await service.get_list(school_id=school_id)


@router.get('/{subgroup_id}', response_model=schemas.subgroup.Subgroup)
async def get_subgroup(
        subgroup_id: int,
        service: SubgroupService = Depends()
):
    return await service.get(subgroup_id)


@router.post(
    '',
    response_model=schemas.subgroup.Subgroup
)
async def create_subgroup(
        subgroup_schema: schemas.subgroup.SubgroupCreate,
        service: SubgroupService = Depends()
):
    return await service.create(subgroup_schema)


@router.patch(
    '/{subgroup_id}',
    response_model=schemas.subgroup.Subgroup
)
async def patch_subgroup(
        subgroup_id: int,
        subgroup_schema: schemas.subgroup.SubgroupUpdate,
        service: SubgroupService = Depends()
):
    return await service.update(subgroup_id, subgroup_schema)


@router.delete(
    '/{subgroup_id}'
)
async def delete_subgroup(
        subgroup_id: int,
        service: SubgroupService = Depends()
):
    return await service.delete(subgroup_id)
