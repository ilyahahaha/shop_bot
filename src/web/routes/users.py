from aiohttp.web import RouteTableDef
from aiohttp_jinja2 import template

from src.common.database import get_session as get_db_session
from src.models import User
from src.schemas.user import UserSchema
from src.utils.web.require_login import require_login

router = RouteTableDef()


@router.get("/")
@require_login
@template("users.jinja2")
async def users_view(_) -> dict[str, list[UserSchema]]:
    """
    (GET) Страница пользователей бота (a.k.a главная)
    :return: dict[str, list[UserSchema]]
    """

    db_session = await get_db_session()
    users = await User.get_all_users(db_session)

    return {"users": users}
