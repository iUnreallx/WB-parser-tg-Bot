from aiogram.fsm.state import StatesGroup, State


class SearchState(StatesGroup):
    search = State()