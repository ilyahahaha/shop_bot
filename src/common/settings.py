from pydantic import PostgresDsn, HttpUrl
from pydantic_settings import SettingsConfigDict, BaseSettings

from src.utils.singleton import singleton


@singleton
class Settings(BaseSettings):
    """
    Конфиг приложения получаемый из env файла.

    Доступные значения:
        - postgres_url - адрес базы данных PostgreSQL
        - bot_token - токен бота
        - base_url - базовый адрес приложения (http://0.0.0.0:8000)
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    postgres_url: PostgresDsn
    bot_token: str
    base_url: HttpUrl
