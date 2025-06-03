from aiogram import Router, types
from aiogram.filters import CommandStart
from states.booking import Booking
from aiogram.fsm.context import FSMContext
from api.flights import search_flights
from keyboards.inline import get_yes_no_kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Booking.origin)
    await message.answer("Привет! Я помогу найти дешевые авиабилеты ✈️")
