from aiogram.fsm.state import State, StatesGroup

class AdminStates(StatesGroup):
    waiting_for_user_id = State()       # waiting for id or @username
    waiting_for_topup_amount = State()  # waiting for topup sum by admin
    waiting_for_broadcast = State() # for alert

class TaskCreateStates(StatesGroup):    # class for custom tasks
    waiting_for_url = State()
    waiting_for_subs = State()
    waiting_for_pay = State()
    waiting_for_desc = State()

class OrderCancelStates(StatesGroup):   # cancel order by admin
    waiting_for_id = State()
