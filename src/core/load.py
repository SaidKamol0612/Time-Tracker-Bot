from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from .config import settings

from aiogram.types import BotCommand


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Botni ishga tushirish"),
        BotCommand(command="help", description="Yordam olish"),
    ]
    await bot.set_my_commands(commands)


_BOT: Bot | None = None


async def _start() -> Bot:
    global _BOT
    _BOT = Bot(
        token=settings.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await set_bot_commands(_BOT)
    return _BOT


async def get_bot() -> Bot:
    global _BOT
    if _BOT is None:
        _BOT = await _start()
    return _BOT
