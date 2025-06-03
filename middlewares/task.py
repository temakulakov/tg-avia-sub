from api.flights import search_flights  # предполагается, что функция импортирована
from aiogram import types
import asyncio
from aiogram.fsm.context import FSMContext


async def monitor_flight_updates(message: types.Message, user_id: int, state: FSMContext, sub: dict):
    origin_code = sub["origin"][1]
    destination_code = sub["destination"][1]
    departure_at = sub["departure_at"]
    one_way = sub["one_way"].lower() == "да"

    while True:
        try:
            result = await search_flights(
                origin=origin_code,
                destination=destination_code,
                departure_at=departure_at,
                way=one_way
            )

            best_prices = result.get("data", [])

            # Пример простой проверки — есть ли вообще билеты
            if best_prices:
                flight = best_prices[0]
                link = flight.get("link", "https://www.aviasales.ru")

                msg = "\n".join([
                    f"✈️ Найден билет!",
                    f"Из {sub['origin'][0]} в {sub['destination'][0]}",
                    f"Цена: {flight['value']} {sub['currency']}",
                    f"Дата вылета: {flight['departure_at']}",
                    f"<a href='{link}'>🔗 Купить билет</a>",
                ])

                await message.bot.send_message(user_id, msg, parse_mode="HTML")

                # Обновляем подписку
                data = await state.get_data()
                subs = data.get("subscribes", [])
                for s in subs:
                    if s == sub:
                        s["found"] = True
                        break
                await state.update_data(subscribes=subs)
                break

        except Exception as e:
            print(f"Ошибка поиска рейсов: {e}")

        await asyncio.sleep(60)  # повтор через 1 минуту
