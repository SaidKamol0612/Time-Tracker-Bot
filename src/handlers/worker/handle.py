import logging
import math

from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.db import db_helper
from core.crud import UserCRUD, SalaryCRUD
from keyboards.reply import (
    START_SHIFT_TXT,
    working_menu,
    END_SHIFT_TXT,
    get_worktypes_kb,
    WORKTYPES,
    WORKER_MENU,
    MY_INFO_TXT,
)
from states.worker_states import WorkerStates
from utils import determine_shift_type

router = Router()


@router.message(F.text == MY_INFO_TXT)
async def my_info(message: Message):
    async with db_helper.session_factory() as session:
        curr = await UserCRUD.get_user_by_tg_id(session, message.from_user.id)
        salary = await SalaryCRUD.get_salary(session, curr.id)
    total = salary.total if salary else 0
    msg = f"👤 <b>Username:</b> {curr.username}\n" f"💸 <b>Oylik:</b> {total}"

    await message.answer(msg)


@router.message(F.text == START_SHIFT_TXT)
async def start_shift(message: Message, state: FSMContext):
    msg_date = message.date
    started_at: datetime = msg_date + timedelta(hours=5)
    shift_type = determine_shift_type(started_at)

    async with db_helper.session_factory() as session:
        curr = await UserCRUD.get_user_by_tg_id(session, message.from_user.id)

    logging.info(f"{curr.username} started shift at {started_at}")

    await state.update_data(started_at=started_at.isoformat())
    await state.update_data(is_chef=False)
    await state.update_data(shift_type=shift_type)
    await state.set_state(WorkerStates.working)

    if shift_type == "day":
        msg = "☀️ Siz kunduzgi smenani boshladingiz.\n"
    else:
        msg = "🌙 Siz tungi smenani boshladingiz.\n"

    await message.answer(
        msg + f"👷‍♂️ Ish vaqti {started_at.hour}:{started_at.minute} da boshlandi.",
        reply_markup=working_menu(is_night=shift_type == "night"),
    )


@router.message(WorkerStates.working, F.text == END_SHIFT_TXT)
async def choose_worktype(message: Message, state: FSMContext):
    msg_date = message.date
    ended_at: datetime = msg_date + timedelta(hours=5)

    await state.update_data(ended_at=ended_at.isoformat())
    await state.set_state(WorkerStates.request_worktype)

    data = await state.get_data()

    if data.get("shift_type") == "day":
        await message.answer(
            "📝 Bugun qanday ishni bajardingiz: ", reply_markup=get_worktypes_kb()
        )
        return

    # Для ночной смены — сразу начисляем деньги
    async with db_helper.session_factory() as session:
        curr = await UserCRUD.get_user_by_tg_id(session, message.from_user.id)

        started_at = datetime.fromisoformat(data["started_at"])
        delta = ended_at - started_at
        hours = math.ceil(delta.total_seconds() / 3600)

        # Night shift hourly salary
        total_sum = hours * 10_000

        today = datetime.now().date()

        shift_type = "Tungi.\n"

        msg = (
            f"📅 <b>Sana:</b> {today}\n"
            f"<b>Ishchi:</b> {curr.username}\n"
            f"<b>Smena:</b> {shift_type}"
            f"<b>Ish boshlandi:</b> {started_at.strftime('%H:%M')} da\n"
            f"<b>Ish tugadi:</b> {ended_at.strftime('%H:%M')} da\n"
            f"🕧 <b>Jami soat:</b> {hours}\n"
            f"<b>Jami pul:</b> {total_sum:,} so'm\n"
        )

        await message.answer(msg, reply_markup=WORKER_MENU)
        await SalaryCRUD.add_to_salary(session, curr.id, total_sum)

        await state.clear()


@router.message(WorkerStates.working)
async def cooked(message: Message, state: FSMContext):
    data = await state.get_data()
    is_chef = data.get("is_chef", False)
    await state.update_data(is_chef=not is_chef)

    msg = (
        "🍽 Siz oshpaz sifatida belgilandingiz."
        if not is_chef
        else "❌ Oshpaz roli bekor qilindi."
    )

    await message.answer(msg, reply_markup=working_menu(is_chef=not is_chef))


@router.message(WorkerStates.request_worktype, F.text.in_(WORKTYPES))
async def end_shift(message: Message, state: FSMContext):
    worktype = message.text.strip()
    salary_per_hour = WORKTYPES.get(worktype)

    async with db_helper.session_factory() as session:
        curr = await UserCRUD.get_user_by_tg_id(session, message.from_user.id)

        data = await state.get_data()

        started_at = datetime.fromisoformat(data.get("started_at"))
        ended_at = datetime.fromisoformat(data.get("ended_at"))
        delta = ended_at - started_at
        hours = math.ceil(delta.total_seconds() / 3600)

        total_sum = hours * salary_per_hour

        if data.get("is_chef"):
            total_sum += 50_000

        msg = (
            f"📅 <b>Sana:</b> {datetime.now().date()}\n"
            f"<b>Ishchi:</b> {curr.username}\n"
            f"<b>Smena:</b> Kunduzgi.\n"
            f"<b>Ish turi:</b> {worktype}\n"
            f"<b>Ish boshlandi:</b> {started_at.strftime('%H:%M')} da\n"
            f"<b>Ish tugadi:</b> {ended_at.strftime('%H:%M')} da\n"
            f"🕧 <b>Jami soat:</b> {hours}\n"
        )

        if data.get("is_chef"):
            msg += "➕ <b>Qo'shimcha:</b> Ovqat tayyorladi (+50 000 so'm).\n"

        msg += f"<b>Jami pul:</b> {total_sum:,} so'm"

        await message.answer(msg, reply_markup=WORKER_MENU)
        await SalaryCRUD.add_to_salary(session, curr.id, total_sum)

        await state.clear()


@router.message(WorkerStates.request_worktype)
async def cancel_ending(message: Message, state: FSMContext):
    await state.set_state(WorkerStates.working)
    data = await state.get_data()

    await message.answer(
        "✅ Ishni tugatish bekor qilindi.",
        reply_markup=working_menu(
            is_chef=data.get("is_chef", False),
            is_night=data.get("shift_type") == "night",
        ),
    )
