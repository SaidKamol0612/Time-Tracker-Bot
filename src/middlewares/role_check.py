from typing import Callable, Awaitable, Dict, Any, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from core.db.models.user import User
from core.enums import UserRoles
from core.db import db_helper


class RoleCheckMiddleware(BaseMiddleware):
    def __init__(self, allowed_roles: list[UserRoles]):
        self.allowed_roles = allowed_roles

    async def __call__(
        self,
        handler: Callable[
            [Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]
        ],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        tg_id = event.from_user.id

        async with db_helper.session_factory() as session:
            stmt = select(User).where(User.tg_id == tg_id)
            user = await session.scalar(stmt) or None

            if not user:
                await event.answer("⛔ Siz ro'yhatdan o'tmagansiz.")
                return

            if user.role not in self.allowed_roles:
                await event.answer("⛔ Sizda bu amal uchun ruxsat yo'q.")
                return

        return await handler(event, data)
