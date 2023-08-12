from base64 import urlsafe_b64encode
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
from src.telegram.router import router as telegram_router
from src.utils.web.username_context_processor import username_context_processor
from src.web.middlewares import check_login
from src.web.router import router as web_router

settings = Settings()


async def bot_startup_callback(bot: Bot) -> None:
    await bot.set_webhook(f"{settings.base_url}webhook")


def init_dispatcher() -> Dispatcher:
    dispatcher = Dispatcher()
    dispatcher["base_url"] = settings.base_url

    dispatcher.startup.register(bot_startup_callback)

    dispatcher.include_router(telegram_router)

    return dispatcher


def init_web(bot: Bot) -> Application:
    web_app = Application()
    web_app["bot"] = bot

    # Подключаем статику
    web_app.add_routes([static("/static", Path(settings.base_dir).parent / "static")])
    web_app["static_root_url"] = "/static"

    # Подключаем роуты
    web_app.add_routes(web_router)

    # Подключаем библиотеки
    session_setup(
        web_app,
        EncryptedCookieStorage(urlsafe_b64encode(settings.secret_key.encode())[:32]),
    )
    jinja2_setup(
        web_app,
        loader=FileSystemLoader(
            Path(settings.base_dir).parent / "templates",
        ),
        context_processors=[username_context_processor],
    )

    web_app.middlewares.append(check_login)

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
