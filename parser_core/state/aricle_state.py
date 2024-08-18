from aiogram.fsm.state import StatesGroup, State


class SearchArticle(StatesGroup):
    search = State()