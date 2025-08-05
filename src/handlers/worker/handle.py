import logging

from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from core.db import db_helper
from core.crud import UserCRUD
from keyboards.reply import START_SHIFT_TXT
from states.worker_states import WorkerStates
from utils import determine_shift_type

router = Router()


@router.message(F.text == START_SHIFT_TXT)
async def start_shift(message: Message, state: FSMContext):
    msg_date = message.date
    started_at: datetime = (msg_date + timedelta(hours=5))
    shift_type = determine_shift_type(started_at)

    async with db_helper.session_factory() as session:
        curr = await UserCRUD.get_user_by_tg_id(session, message.from_user.id)

    logging.info(f"{curr.username} started shift at {started_at}")

    await state.update_data(started_at=started_at.isoformat())
    await state.set_state(WorkerStates.working)

    if shift_type == "day":
        msg = "☀️ Siz kunduzgi smenani boshladingiz.\n"
    else:
        msg = "🌙 Siz tungi smenani boshladingiz.\n"

    await message.answer(
        msg + f"👷‍♂️ Ish vaqti {started_at.hour}:{started_at.minute} da boshlandi."
    )
