from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud


async def investing(
    session: AsyncSession
):
    opened_charity_projects = (
        await charity_project_crud.get_opened_charity_projects(
            session
        )
    )

    not_invested_donations = await donation_crud.get_not_invested_donations(
        session
    )

    if not opened_charity_projects or not not_invested_donations:
        return

    while len(opened_charity_projects) > 0 and len(not_invested_donations) > 0:
        possible_amount_to_donate = (
            opened_charity_projects[0].full_amount
            - opened_charity_projects[0].invested_amount
        )
        donation_amount = (
            not_invested_donations[0].full_amount
            - not_invested_donations[0].invested_amount
        )
        amount_to_donate = min(possible_amount_to_donate, donation_amount)
        opened_charity_projects[0].invested_amount += amount_to_donate
        not_invested_donations[0].invested_amount += amount_to_donate
        if (opened_charity_projects[0].invested_amount ==
                opened_charity_projects[0].full_amount):
            opened_charity_projects[0].fully_invested = True
            opened_charity_projects[0].close_date = datetime.now()
            opened_charity_projects.pop(0)
        if (not_invested_donations[0].invested_amount ==
                not_invested_donations[0].full_amount):
            not_invested_donations[0].fully_invested = True
            not_invested_donations[0].close_date = datetime.now()
            not_invested_donations.pop(0)
    await session.commit()
