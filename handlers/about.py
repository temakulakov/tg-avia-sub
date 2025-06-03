from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from states.booking import Booking
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command('about'))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.set_state(Booking.origin)
    await message.answer("Привет! Я помогу найти дешевые авиабилеты ✈️")
