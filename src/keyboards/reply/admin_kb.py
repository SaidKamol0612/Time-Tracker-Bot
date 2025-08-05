from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from core.db.models import User

FULL_OVERVIEW_TXT = "📊 To'liq hisobot"
PAY_SALARY_TXT = "💸 Oylik to'lash"

ADMIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=FULL_OVERVIEW_TXT)],
        [KeyboardButton(text=PAY_SALARY_TXT)],
    ],
    resize_keyboard=True,
)


def show_workers_kb(users: list[User]):
    keyboard = ReplyKeyboardBuilder()

    for user in users:
        keyboard.add(KeyboardButton(text=user.username))
    keyboard.add(KeyboardButton(text="🚫 Bekor qilish"))

    return keyboard.adjust(1).as_markup(resize_keyboard=True)
