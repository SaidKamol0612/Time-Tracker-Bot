from aiogram import Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import main_router

from core.load import get_bot

dp = Dispatcher(storage=MemoryStorage())


async def start_bot() -> None:
    bot = get_bot()

    dp.include_router(main_router)

    await dp.start_polling(bot)


@dp.message(CommandStart())
async def cmd_start(message: Message):
    user = message.from_user

    start_msg = f"Assalomu alaykum @{user.username}!\n"

    await message.answer(text=start_msg)
