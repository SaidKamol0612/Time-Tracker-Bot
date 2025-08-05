from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.reply import (
    FULL_OVERVIEW_TXT,
    PAY_SALARY_TXT,
    show_workers_kb,
    ADMIN_MENU,
)
from core.db import db_helper
from core.crud import UserCRUD, SalaryCRUD
from states.admin_workers import AdminStates

router = Router()


@router.message(F.text == FULL_OVERVIEW_TXT)
async def full_overview(message: Message):

    async with db_helper.session_factory() as session:
        users = await UserCRUD.get_workers(session)
    if len(users) < 1:
        await message.answer("⚠️ Botda ro'yhatdan o'tgan ishchilar yo'q.")

    msg = ""
    for i, user in enumerate(users, start=1):
        msg += f"{i}. <b>👤Ishchi (username):</b> {user.username}\n"

        salary = await SalaryCRUD.get_or_create_salary(session, user.id)
        msg += f"\t<b>Oyligi:</b>{salary.total}\n"

    msg += f"<b>Jami ishchilar:</b> {len(users)}"

    await message.answer(msg)


@router.message(F.text == PAY_SALARY_TXT)
async def pay_salary(message: Message, state: FSMContext):
    async with db_helper.session_factory() as session:
        users = await UserCRUD.get_workers(session)
    if len(users) < 1:
        await message.answer("⚠️ Botda ro'yhatdan o'tgan ishchilar yo'q.")

    await state.set_state(AdminStates.choose_worker)
    await message.answer(
        "O'yligini to'lamoqchi bo'lgan ishchini tanlang: ",
        reply_markup=show_workers_kb(users),
    )


@router.message(AdminStates.choose_worker)
async def choose_worker(message: Message):
    async with db_helper.session_factory() as session:
        users = await UserCRUD.get_workers(session)

    usernames = [user.username for user in users]
    username = message.text.strip()
    if username == "🚫 Bekor qilish":
        await message.answer("✅ Bekor qilindi", reply_markup=ADMIN_MENU)
        return
    elif username not in usernames:
        await message.answer("⚠️ Botda bunday ishchi ro'yhatdan o'tmagan.")
        return

    user_id = next((u.id for u in users if u.username == username))

    await SalaryCRUD.set_null(session, user_id)

    await message.answer(
        "✅ O'ylik muavaffaqiyatli bazadan chiqazib tashlandi.", reply_markup=ADMIN_MENU
    )
