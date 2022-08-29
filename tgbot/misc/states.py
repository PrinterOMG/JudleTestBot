from aiogram.dispatcher.filters.state import State, StatesGroup


class PersonalInfoState(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_city = State()
    waiting_for_phone = State()
