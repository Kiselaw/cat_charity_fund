from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_before_delete,
                                check_charity_project_before_edit,
                                check_charity_project_exists,
                                check_charity_project_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investing import investing

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_charity_project_name_duplicate(charity_project.name, session)
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session
    )
    await investing(session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Доступно всем пользователям."""
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        charity_project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    await check_charity_project_before_edit(
        charity_project_id,
        obj_in,
        session
    )
    if obj_in.name is not None:
        await check_charity_project_name_duplicate(obj_in.name, session)
    updated_charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    await investing(session)
    await session.refresh(updated_charity_project)
    return updated_charity_project


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        charity_project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(
        charity_project_id,
        session
    )
    await check_charity_project_before_delete(
        charity_project_id,
        session
    )
    charity_project = await charity_project_crud.remove(
        charity_project,
        session
    )
    return charity_project
