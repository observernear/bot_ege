from aiogram.fsm.state import State, StatesGroup


class FSMsubject(StatesGroup):
    subject = State()
    problems = State()
