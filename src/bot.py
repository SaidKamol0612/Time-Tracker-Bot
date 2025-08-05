from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router as main_router

from core.load import get_bot
from core.config import settings
from core.crud import UserCRUD
from core.db import db_helper

dp = Dispatcher(storage=MemoryStorage())


async def start_bot() -> None:
    bot = get_bot()

    dp.include_router(main_router)

    await dp.start_polling(bot)


@dp.message(F.text.startswith("/start"))
async def cmd_start(message: Message):
    args = message.text.split()
    token = args[1] if len(args) > 1 else ""
    name = message.from_user.first_name or message.from_user.username
    tg_id = message.from_user.id

    msg = f"Assalomu alaykum, {name}.\n" "Botimizga xush kelibsiz!\n"
    admin = token == settings.admin.token
    if admin:
        msg += "✅ Siz admin sifatida ro'yhatdan o'tdingiz."

    async with db_helper.session_factory() as session:
        await UserCRUD.set_user(session, name, tg_id, admin)

    await message.answer(msg)
