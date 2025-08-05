from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    choose_worker = State()
