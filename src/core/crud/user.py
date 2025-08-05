from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.models import User
from core.enums import UserRoles


class UserCRUD:
    @staticmethod
    async def set_user(
        session: AsyncSession, username: str, tg_id: int, is_admin: bool = False
    ) -> User:
        stmt = select(User).where(User.tg_id == tg_id)
        user = await session.scalar(stmt) or None

        role = UserRoles.ADMIN if is_admin else UserRoles.WORKER
        if user:
            user.username = username
        else:
            user = User(
                tg_id=tg_id,
                username=username,
                role=role,
            )

            session.add(user)

        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_user_by_tg_id(session: AsyncSession, tg_id: int) -> User | None:
        stmt = select(User).where(User.tg_id == tg_id)
        res = await session.scalar(stmt)
        return res or None
