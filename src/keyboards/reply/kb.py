from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

REMOVER = ReplyKeyboardRemove()

START_SHIFT_TXT = "▶️ Ishni boshlash"

START_SHIFT = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=START_SHIFT_TXT)],
        [KeyboardButton(text="📊 Hisobotni ko‘rish")],
    ],
    resize_keyboard=True,
)

