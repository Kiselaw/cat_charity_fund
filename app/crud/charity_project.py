from typing import Optional

from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_opened_charity_projects(self, session):
        opened_charity_projects = await session.execute(
            select(CharityProject).where(
                not_(CharityProject.fully_invested)
            ).order_by(CharityProject.create_date)
        )
        opened_charity_projects = opened_charity_projects.scalars().all()
        return opened_charity_projects


charity_project_crud = CRUDCharityProject(CharityProject)
