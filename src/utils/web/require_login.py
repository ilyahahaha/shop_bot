from typing import Callable, Awaitable

from aiohttp.web import Request, StreamResponse


def require_login(
    func: Callable[[Request], Awaitable[StreamResponse]]
) -> Callable[[Request], Awaitable[StreamResponse]]:
    """
    Декоратор для эндпоинтов требующих авторизации.
    :param func:
    :return: Callable[[Request], Awaitable[StreamResponse]]
    """
    func.__require_login__ = True  # type: ignore

    return func
