from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_user_id = State()  # waiting for id or @username

class AdminStates(StatesGroup):
    waiting_for_user_id = State()
    waiting_for_topup_amount = State()  # waiting for topup sum by admin
    