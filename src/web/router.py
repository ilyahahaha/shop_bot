import json

from aiohttp.web import RouteTableDef, Request, HTTPSeeOther, Response, HTTPUnauthorized
from aiohttp.web_exceptions import HTTPBadRequest
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from pydantic import ValidationError

from src.common.database import Database
from src.models import Admin, User
from src.schemas.admin import LoginAdminSchema
from src.schemas.toast import Toast
from src.schemas.user import UserSchema
from src.utils.web.password import verify_password
from src.utils.web.require_login import require_login

database = Database()
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


@router.get("/")
@require_login
@template("users.jinja2")
async def users_view(_) -> dict[str, list[UserSchema]]:
    """
    (GET) Страница пользователей бота (a.k.a главная)
    :return: dict[str, list[UserSchema]]
    """

    db_session = await database.get_session()
    users = await User.get_all_users(db_session)

    return {"users": users}


@router.post("/login")
async def login_post(request: Request) -> Response:
    """
    (POST) Эндпоинт авторизации
    :param request: Запрос от клиента
    :return: Response
    """

    db_session = await database.get_session()
    session = await get_session(request)
    form = await request.post()

    try:
        data = LoginAdminSchema.model_validate(form)
        admin = await Admin.find_by_username(db_session, data.login)

        if admin is None or not verify_password(data.password, admin.hashed_password):
            raise HTTPUnauthorized(
                headers={
                    "HX-Trigger": json.dumps(
                        {
                            "toast": Toast(
                                message="Неверный логин или пароль", error=True
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
                "HX-Trigger": json.dumps(
                    {
                        "toast": Toast(
                            message="Неверные параметры запроса", error=True
                        ).model_dump()
                    }
                )
            },
        )


@router.get("/logout")
@require_login
async def logout_get(request: Request) -> None:
    """
    (POST) Эндпоинт выхода из аккаунта
    :param request: Запрос от клиента
    :return: None
    """

    session = await get_session(request)
    session["username"] = None

    raise HTTPSeeOther(location="/login")
