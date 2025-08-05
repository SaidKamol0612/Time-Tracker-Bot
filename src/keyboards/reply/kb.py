from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

REMOVER = ReplyKeyboardRemove()

START_SHIFT_TXT = "▶️ Ishni boshlash"
MY_INFO_TXT = "🗃️ Mening ma'lumotlarim"

WORKER_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=START_SHIFT_TXT)],
        [KeyboardButton(text=MY_INFO_TXT)],
    ],
    resize_keyboard=True,
)

END_SHIFT_TXT = "⏹️ Ishni tugatish"


def working_menu(is_chef: bool = False, is_night: bool = False):
    chef_msg = "🥗 Ovqat"
    if is_chef:
        chef_msg += ": ✅"

    keyboard = ReplyKeyboardBuilder(
        markup=[
            [KeyboardButton(text=END_SHIFT_TXT)],
        ],
    )
    if not is_night:
        keyboard.add(KeyboardButton(text=chef_msg))

    return keyboard.adjust(1).as_markup(resize_keyboard=True)


WORKTYPES = {"🥣 Xamirchi": 20_000, "🔥 Pechkachi": 15_000, "🏭 Teruvchi": 12_000}


def get_worktypes_kb():
    worktypes = WORKTYPES.items()
    keyboard = ReplyKeyboardBuilder()

    for type, _ in worktypes:
        keyboard.add(KeyboardButton(text=type))
    keyboard.add(KeyboardButton(text="🚫 Bekor qilish"))
    return keyboard.adjust(1).as_markup(resize_keyboard=True)
