import logging

from fastapi import APIRouter, Depends

from lyceum_backend import schemas
from lyceum_backend.services.school import SchoolService


logger = logging.getLogger(__name__)
router = APIRouter(
    prefix='/api/schools',
    tags=["Schools"],
)


@router.get(
    '/',
    response_model=schemas.school.School
)
async def get_schools(
        service: SchoolService = Depends()
):
    return await service.get_all()


@router.get('/{school_id}', response_model=schemas.school.School)
async def get_school(
        school_id: int,
        service: SchoolService = Depends()
):
    return await service.get(school_id)


@router.post(
    '',
    response_model=schemas.school.School
)
async def create_school(
        school_schema: schemas.school.SchoolCreate,
        service: SchoolService = Depends()
):
    return await service.create_school(school_schema)


@router.patch(
    '/{school_id}',
    response_model=schemas.school.School
)
async def patch_school(
        school_id: int,
        school_schema: schemas.school.SchoolUpdate,
        service: SchoolService = Depends()
):
    return await service.update_school(school_id, school_schema)


@router.delete(
    '/{school_id}'
)
async def delete_school(
        school_id: int,
        service: SchoolService = Depends()
):
    return await service.delete(school_id)
