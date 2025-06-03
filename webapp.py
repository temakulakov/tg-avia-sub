import logging
from fastapi import FastAPI
import asyncio

from bot_instance import bot, dp
from handlers import start, create, about, subscription_list, unsubscribe
from middlewares.redis import setup_redis

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Запуск Telegram-бота через FastAPI")
    

    dp.include_routers(
        start.router,
        create.router,
        about.router,
        subscription_list.router,
        unsubscribe.router,
    )

    await setup_redis(dp)
    asyncio.create_task(dp.start_polling(bot))

@app.get("/")
async def root():
    return {"message": "Бот работает"}
