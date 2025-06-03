import asyncio
from datetime import datetime, date, timedelta

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from api.flights import get_locations_by_city_name
from keyboards.inline import get_yes_no_kb, destonation_at_kb, destonation_to_kb, departure_to_kb
from middlewares.task import monitor_flight_updates
from states.booking import Booking

router = Router()


@router.message(Command('create'))
async def cmd_create(message: types.Message, state: FSMContext):
    await state.set_state(Booking.origin)
    await message.answer("Откуда вылетаете? Введите город на русском (без сокращений):",
                         reply_markup=destonation_at_kb())


@router.message(Booking.origin)
async def set_origin(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    results = await get_locations_by_city_name(user_input)

    if not results:
        await message.answer("❌ Город не найден. Попробуйте ещё раз.")
        return

    city = next((item for item in results if item["type"] == "city"), None)

    if not city:
        await message.answer("❌ Не удалось определить IATA-код. Введите корректное название города.")
        return

    await state.update_data(origin=[user_input, city["code"]])
    await state.set_state(Booking.destination)

    await message.answer(
        f"✅ Город найден: <b>{city['name']}</b> ({city['code']})\nКуда хотите полететь?",
        reply_markup=destonation_to_kb(),
        parse_mode="HTML"
    )


@router.message(Booking.destination)
async def set_destination(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    results = await get_locations_by_city_name(user_input)

    if not results:
        await message.answer("❌ Город назначения не найден. Попробуйте ещё раз.")
        return

    city = next((item for item in results if item["type"] == "city"), None)

    if not city:
        await message.answer("❌ Не удалось определить IATA-код. Введите корректное название города.")
        return

    await state.update_data(destination=[user_input, city["code"]])
    await state.set_state(Booking.departure_at)

    await message.answer(
        f"✅ Город назначения: <b>{city['name']}</b> ({city['code']})\nКогда вылет? Введите дату в формате ДД.ММ.ГГГГ",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )


@router.message(Booking.departure_at)
async def set_departure_at(message: types.Message, state: FSMContext):
    user_input = message.text.strip()

    # Попытка распарсить дату из разных форматов
    parsed_date = None
    formats_to_try = ["%d.%m.%Y", "%d.%m.%y", "%-d.%-m.%Y", "%-d.%-m.%y", "%d.%m", "%-d.%-m"]

    for fmt in formats_to_try:
        try:
            parsed = datetime.strptime(user_input, fmt)
            # Если пользователь не указал год, подставим текущий
            if "%Y" not in fmt and "%y" not in fmt:
                parsed = parsed.replace(year=date.today().year)
            parsed_date = parsed
            break
        except ValueError:
            continue

    # Если ничего не распарсилось
    if not parsed_date:
        await message.answer("❌ Неверный формат даты. Введите в формате ДД.ММ.ГГГГ (например: 06.07.2025 или 6.7.25)")
        return

    # Проверка: дата не может быть в прошлом
    today = datetime.today().date()
    if parsed_date.date() < today:
        await message.answer("❌ Нельзя указывать дату в прошлом. Введите актуальную дату.")
        return

    # Всё ок — сохраняем в формате ДД.ММ.ГГГГ
    formatted_date = parsed_date.strftime("%d.%m.%Y")
    await state.update_data(departure_at=formatted_date)
    await state.set_state(Booking.one_way)

    await message.answer("Летим туда и обратно?", reply_markup=get_yes_no_kb())


@router.message(Booking.one_way)
async def set_one_way(message: types.Message, state: FSMContext):
    user_input = message.text.strip().lower()

    if user_input not in ["да", "нет"]:
        await message.answer("❌ Пожалуйста, выберите 'Да' или 'Нет' с клавиатуры.")
        return

    await state.update_data(one_way=user_input.capitalize())  # сохраняем "Да" или "Нет" с заглавной
    await state.set_state(Booking.departure_to)
    await message.answer("На сколько дней?", reply_markup=departure_to_kb())


@router.message(Booking.departure_to)
async def confirm_subscription(message: types.Message, state: FSMContext):
    user_input = message.text.strip()
    digits = ''.join(filter(str.isdigit, user_input))

    if not digits:
        await message.answer("❌ Укажите количество дней (например, '10 дней' или просто '10').")
        return

    days = int(digits)

    data = await state.get_data()
    departure_date_str = data.get("departure_at")

    try:
        departure_date = datetime.strptime(departure_date_str, "%d.%m.%Y")
        return_date = departure_date + timedelta(days=days)
        return_date_str = return_date.strftime("%d.%m.%Y")
    except Exception:
        await message.answer("❌ Ошибка при расчёте даты возвращения.")
        return

    # Сохраняем дату возвращения
    await state.update_data(departure_to=return_date_str)
    await state.set_state(Booking.is_subcribe)

    text = "\n".join([
        "Ну балдёж, подписка почти готова! Осталось только подтвердить",
        f"Направление: <b>{data['origin'][0]}</b> - <b>{data['destination'][0]}</b>",
        f"Тип билета: <b>{'Туда-обратно' if data.get('one_way') == 'Да' else 'В одну сторону'}</b>",
        f"Вылет: <b>{departure_date_str}</b>",
        f"Возврат: <b>{return_date_str}</b>",
    ])

    await message.answer(text, reply_markup=get_yes_no_kb(), parse_mode="HTML")


@router.message(Booking.is_subcribe)
async def save_subscription(message: types.Message, state: FSMContext):
    answer = message.text.strip().lower()

    if answer != "да":
        await message.answer("❌ Подписка не сохранена.")
        await state.clear()
        return
    # Запускаем фоновую задачу

    # Получаем все текущие данные
    data = await state.get_data()

    # Подготовим объект подписки (то, что нужно сохранить)
    # Преобразуем даты
    try:
        departure_at_iso = datetime.strptime(data.get("departure_at"), "%d.%m.%Y").strftime("%Y-%m-%d")
        departure_to_iso = datetime.strptime(data.get("departure_to"), "%d.%m.%Y").strftime("%Y-%m-%d")
    except Exception:
        await message.answer("❌ Ошибка при преобразовании дат.")
        await state.clear()
        return

    new_sub = {
        "origin": data.get("origin"),
        "destination": data.get("destination"),
        "departure_at": departure_at_iso,
        "one_way": data.get("one_way"),
        "departure_to": departure_to_iso,
        "currency": data.get("currency", "rub"),
        "found": False,
    }

    asyncio.create_task(
        monitor_flight_updates(
            message=message,
            user_id=message.from_user.id,
            state=state,
            sub=new_sub
        )
    )

    # Получаем текущий список подписок, если есть
    current_subs = data.get("subscribes", [])

    if not isinstance(current_subs, list):
        current_subs = []

    current_subs.append(new_sub)

    # Обнуляем всё кроме списка подписок
    await state.clear()
    await state.update_data(subscribes=current_subs)

    await message.answer("✅ Подписка сохранена! Хотите создать ещё одну? Напишите /create или /start.",
                         reply_markup=ReplyKeyboardRemove())
