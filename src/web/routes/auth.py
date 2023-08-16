from json import dumps

from aiohttp.web import Request, RouteTableDef, Response
from aiohttp.web_exceptions import HTTPSeeOther, HTTPUnauthorized, HTTPBadRequest
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from pydantic import ValidationError

from src.common.database import get_session as get_db_session
from src.models import Admin
from src.schemas.admin import LoginAdminSchema
from src.schemas.toast import ToastSchema
from src.utils.web.password import verify_password
from src.utils.web.require_login import require_login

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

    db_session = await get_db_session()
    session = await get_session(request)
    form = await request.post()

    try:
        data = LoginAdminSchema.model_validate(form)
        admin = await Admin.find_by_username(db_session, data.login)

        if admin is None or not verify_password(data.password, admin.hashed_password):
            raise HTTPUnauthorized(
                headers={
                    "HX-Trigger": dumps(
                        {
                            "toast": ToastSchema(
                                message="Неверный логин или пароль"
                            ).model_dump()
                        }
                    )
                },
            )

        session["username"] = data.login

        return Response(
            status=200, text="Вы успешно авторизовались", headers={"HX-Redirect": "/"}
        )
    except ValidationError:
        raise HTTPBadRequest(
            headers={
                "HX-Trigger": dumps(
                    {
                        "toast": ToastSchema(
                            message="Неверные параметры запроса"
                        ).model_dump()
                    }
                )
            },
        )


@router.get("/logout")
@require_login
async def logout_view(request: Request) -> None:
    """
    (POST) Эндпоинт выхода из аккаунта
    :param request: Запрос от клиента
    :return: None
    """

    session = await get_session(request)
    session["username"] = None

    raise HTTPSeeOther(location="/login")
