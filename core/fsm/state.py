from aiogram.fsm.state import State, StatesGroup


class FSMsubject(StatesGroup):
    subject = State()
    problems = State()


class FSMadmin(StatesGroup):
    message_push = State()


class FSMuser(StatesGroup):
    donate = State()
