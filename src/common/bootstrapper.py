from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import Application
from aiohttp.web import run_app
from aiohttp.web import static
from aiohttp_jinja2 import setup as jinja2_setup
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from jinja2 import FileSystemLoader

from src.common.settings import Settings
from src.utils.web.username_context_processor import username_context_processor
from src.web.routes import router

settings = Settings()


async def bot_startup_callback(bot: Bot) -> None:
    await bot.set_webhook(f"{settings.base_url}/webhook")


def init_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher["base_url"] = settings.base_url

    dispatcher.startup.register(bot_startup_callback)

    return dispatcher


def init_web(bot: Bot) -> Application:
    web_app = Application()
    web_app["bot"] = bot

    # Подключаем статику
    web_app.add_routes([static("/static", Path(settings.base_dir).parent / "static")])
    web_app["static_root_url"] = "/static"

    # Подключаем роуты
    web_app.add_routes(router)

    # Подключаем библиотеки
    session_setup(web_app, EncryptedCookieStorage(b"Thirty  two  length  bytes  key."))
    jinja2_setup(
        web_app,
        loader=FileSystemLoader(
            Path(settings.base_dir).parent / "templates",
        ),
        context_processors=[username_context_processor],
    )

    return web_app


def bootstrap() -> None:
    bot = Bot(token=settings.bot_token, parse_mode="HTML")

    dispatcher = init_dispatcher()
    web_app = init_web(bot)

    SimpleRequestHandler(bot=bot, dispatcher=dispatcher).register(
        web_app, path="/webhook"
    )
    setup_application(web_app, dispatcher, bot=bot)

    run_app(web_app, host="127.0.0.1", port=8081)
