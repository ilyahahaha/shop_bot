import json

from aiohttp.web import RouteTableDef, Request, HTTPSeeOther, Response
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from pydantic import ValidationError

from src.web.schemas.admin import Admin

router = RouteTableDef()


@router.get("/login")
@template("login.jinja2")
async def login_view(request: Request) -> dict:
    """
    (GET) Страница входа
    :param request: Запрос от клиента
    :return: dict
    """

    session = await get_session(request)

    if session.get("username") is not None:
        raise HTTPSeeOther(location="/")

    return {}


@router.post("/login")
async def login_post(request: Request) -> Response:
    """
    (POST) Эндпоинт авторизации
    :param request: Запрос от клиента
    :return: Response
    """

    session = await get_session(request)
    form = await request.post()

    try:
        data = Admin.model_validate(form)

        # TODO: работа с базой данных
        session["username"] = data.login

        raise HTTPSeeOther(location="/")
    except ValidationError:
        return Response(
            status=204,
            headers={
                "HX-Trigger": json.dumps({"message": "Неверные параметры запроса"})
            },
        )


@router.get("/logout")
async def logout(request: Request) -> None:
    """
    (POST) Эндпоинт выхода из аккаунта
    :param request: Запрос от клиента
    :return: None
    """

    session = await get_session(request)
    session["username"] = None

    raise HTTPSeeOther(location="/login")
