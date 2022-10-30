from operator import not_
from typing import Optional

from sqlalchemy import not_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User
from app.models.donation import Donation


class CRUDDonation(CRUDBase):

    async def get_user_donations(
            self, session: AsyncSession, user: User
    ):
        reservations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return reservations.scalars().all()

    async def get_not_invested_donations(self, session):
        not_invested_donations = await session.execute(
            select(Donation).where(
                not_(Donation.fully_invested)
                ).order_by(Donation.create_date)
        )
        not_invested_donations = not_invested_donations.scalars().all()
        return not_invested_donations


donation_crud = CRUDDonation(Donation)
