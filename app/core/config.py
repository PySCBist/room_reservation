import os

from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    app_title: str = 'Бронирование переговорок'
    description: str = 'Здесь будем бронировать переговорки'
    database_url: str = os.environ["DATABASE_URL"]
    secret: str = 'SECRET'
    redis_host: str
    redis_port: int

    class Config:
        env_file = '../.env'


settings = Settings()
