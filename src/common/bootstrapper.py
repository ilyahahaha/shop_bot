from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp.web import run_app
from aiohttp.web_app import Application

from src.common.settings import Settings

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
