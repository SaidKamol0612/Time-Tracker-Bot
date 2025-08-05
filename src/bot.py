from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import main_router

from core.load import get_bot
from core.config import settings

dp = Dispatcher(storage=MemoryStorage())


async def start_bot() -> None:
    bot = get_bot()

    dp.include_router(main_router)

    await dp.start_polling(bot)


@dp.message(F.text.startswith("/start"))
async def cmd_start(message: Message):
    args = message.text.split()
    token = args[1] if len(args) > 1 else ""
    name = message.from_user.first_name

    msg = f"Assalomu alaykum, {name}.\n" "Botimizga xush kelibsiz!\n"
    if token == settings.admin.token:
        # TODO: write logic to adding admin to db
        msg += "✅ Siz admin sifatida ro'yhatdan o'tdingiz."
    await message.answer(msg)
