from os import path

from pydantic import PostgresDsn, HttpUrl, DirectoryPath
from pydantic_settings import SettingsConfigDict, BaseSettings

from src.utils.singleton import singleton


@singleton
class Settings(BaseSettings):
    """
    Конфиг приложения получаемый из env файла.

    Доступные значения:
        - base_dir - [стандартное значение] директория корневого модуля
        - postgres_url - адрес базы данных PostgreSQL
        - secret_key - ключ для шифрования куки и пароля
        - bot_token - токен бота
        - base_url - базовый адрес приложения (http://0.0.0.0:8000)
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    base_dir: DirectoryPath = path.dirname(path.dirname(__file__))

    postgres_url: PostgresDsn
    secret_key: str
    bot_token: str
    base_url: HttpUrl
