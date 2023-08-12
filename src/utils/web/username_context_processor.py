from aiohttp.web import Request
from aiohttp_session import get_session


async def username_context_processor(request: Request) -> dict[str, str | None]:
    """
    Примешивание пользователя из сессии в контекст каждого Jinja шаблона
    :param request:
    :return: dict[str, str | None]
    """
    session = await get_session(request)
    username = session.get("username")

    return {"username": username}
