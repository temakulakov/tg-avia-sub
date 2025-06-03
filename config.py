from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    API_TOKEN: str
    API_URL: str
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379

    class Config:
        env_file = '.env'

config = Settings()
