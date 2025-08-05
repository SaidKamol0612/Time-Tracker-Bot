__all__ = ("router",)

from aiogram import Router

from core.enums import UserRoles
from middlewares.role_check import RoleCheckMiddleware

from .handle import router as handler

router = Router()

router.include_router(handler)

router.message.middleware(RoleCheckMiddleware([UserRoles.WORKER]))
