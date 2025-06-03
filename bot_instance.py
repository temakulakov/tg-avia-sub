from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import config

redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT)
storage = RedisStorage(redis=redis)

bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)
