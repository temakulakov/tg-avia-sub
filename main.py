import asyncio
import logging

from bot_instance import bot, dp
from handlers import start, create, about, subscription_list, unsubscribe
from middlewares.redis import setup_redis

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    logger.info("Бот запускается...")


    dp.include_routers(
        start.router,
        unsubscribe.router,
        create.router,
        about.router,
        subscription_list.router,
    )

    await setup_redis(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
