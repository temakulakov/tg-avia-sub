from aiogram.utils.markdown import hbold, hitalic
from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from states.booking import Booking
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("subscription_list"))
async def cmd_subscription_list(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subscriptions = data.get("subscribes", [])

    if not subscriptions:
        await message.answer("🗂 Подписок нет. Ничего не найдено 😢")
        return

    for i, sub in enumerate(subscriptions, start=1):
        one_way_text = "Туда-обратно" if sub.get("one_way") == "Да" else "В одну сторону"

        text = f"""
        📦 <b>Подписка #{i}</b>
        "{hbold('Откуда')}: {sub['origin'][0]} ({sub['origin'][1]})"
        "{hbold('Куда')}: {sub['destination'][0]} ({sub['destination'][1]})"
        <b>Вылет:</b> {sub.get("departure_at")}
        <b>Тип билета:</b> {one_way_text}
        {f"<b>Возврат:</b> {sub.get('departure_to')}" if one_way_text == "Туда-обратно" else ""}
        <b>Валюта:</b> {sub.get("currency", "rub")}
        """.strip()

        await message.answer(text, parse_mode="HTML")

