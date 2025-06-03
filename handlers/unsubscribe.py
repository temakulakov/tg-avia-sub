from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from states.booking import Booking
from aiogram.fsm.context import FSMContext
from keyboards.inline import get_yes_no_kb

router = Router()

@router.message(Command('unsubscribe'))
async def ask_unsubscribe_confirmation(message: types.Message, state: FSMContext):
    await state.set_state(Booking.is_delete)  # временно используем это состояние
    await message.answer(
        "⚠️Вы уверены, что хотите удалить все подписки?",
        reply_markup=get_yes_no_kb()
    )
@router.message(Booking.is_delete)
async def confirm_unsubscribe(message: types.Message, state: FSMContext):
    user_input = message.text.strip().lower()

    if user_input == "да":
        await state.update_data(subscribes=[])
        await message.answer("✅ Все подписки удалены.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("❌ Удаление отменено.", reply_markup=types.ReplyKeyboardRemove())

    await state.clear()
