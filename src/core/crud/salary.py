from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import Salary


class SalaryCRUD:
    @staticmethod
    async def add_to_salary(session: AsyncSession, user_id: int, daily_salary: int):
        stmt = select(Salary).where(Salary.user_id == user_id)
        salary = await session.scalar(stmt)

        if salary:
            salary.total = salary.total + daily_salary
            salary.last_entered = daily_salary
        else:
            salary = Salary(
                user_id=user_id, total=daily_salary, last_entered=daily_salary
            )
            session.add(salary)

        await session.commit()
        await session.refresh(salary)

    @staticmethod
    async def get_or_create_salary(session: AsyncSession, user_id: int):
        stmt = select(Salary).where(Salary.user_id == user_id)
        salary = await session.scalar(stmt)

        if not salary:
            salary = Salary(user_id=user_id)
            session.add(salary)
            await session.commit()
            await session.refresh(salary)

        return salary

    @staticmethod
    async def set_null(session: AsyncSession, user_id: int) -> bool:
        stmt = select(Salary).where(Salary.user_id == user_id)
        salary = await session.scalar(stmt)

        if salary:
            salary.total = 0
            await session.commit()
            await session.refresh(salary)

        return True
