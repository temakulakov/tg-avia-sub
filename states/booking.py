from aiogram.fsm.state import StatesGroup, State

class Booking(StatesGroup):
    origin = State()
    destination = State()
    departure_at = State()
    one_way = State()
    departure_to = State()
    currency = State()
    is_subcribe = State()
    subscribes = State()

    is_delete = State()
