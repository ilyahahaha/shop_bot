from typing import Callable, Awaitable

from aiohttp.web import StreamResponse, middleware, Request, HTTPSeeOther
from aiohttp_session import get_session


@middleware
async def check_login(
    request: Request, handler: Callable[[Request], Awaitable[StreamResponse]]
) -> StreamResponse:
    login_required = getattr(handler, "__require_login__", False)

    session = await get_session(request)
    username = session.get("username")

    if login_required:
        if not username:
            raise HTTPSeeOther(location="/login")

    return await handler(request)
