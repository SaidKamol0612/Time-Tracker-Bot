__all__ = ("router",)

from aiogram import Router

from core.enums import UserRoles
from middlewares.role_check import RoleCheckMiddleware

router = Router()

router.message.middleware(RoleCheckMiddleware([UserRoles.WORKER]))
