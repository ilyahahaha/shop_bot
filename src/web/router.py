from json import dumps

from aiohttp.web import RouteTableDef, Request, HTTPSeeOther, Response, HTTPUnauthorized
from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound
from aiohttp_jinja2 import template
from aiohttp_session import get_session
from pydantic import ValidationError

from src.common.database import get_session as get_db_session
from src.common.exceptions import DatabaseAlreadyExistsExceptions
from src.models import Admin, User, Category
from src.schemas.admin import LoginAdminSchema
from src.schemas.category import CategorySchema, EditCategorySchema
from src.schemas.toast import ToastSchema
from src.schemas.user import UserSchema
from src.utils.web.password import verify_password
from src.utils.web.require_login import require_login

router = RouteTableDef()


# region ROUTES: /login


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


# endregion


# region ROUTES: /logout


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


# endregion


# region ROUTES: /


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


# endregion


# region ROUTES: /categories


@router.get("/categories")
@require_login
@template("categories.jinja2")
async def categories_view(_) -> dict[str, list[CategorySchema]]:
    """
    (GET) Страница категорий товаров
    :return: dict[str, list[CategorySchema]]
    """

    db_session = await get_db_session()
    categories = await Category.get_all_categories(db_session)

    return {"categories": categories}


@router.post("/categories")
@require_login
async def categories_post(request: Request) -> Response:
    """
    (POST) Эндпоинт создания категории
    :param request: Запрос от клиента
    :return: Response
    """

    db_session = await get_db_session()
    form = await request.post()

    try:
        data = EditCategorySchema.model_validate(form)
        category = Category(name=data.name)

        await category.save(db_session)

        return Response(
            status=200,
            text="Категория создана",
            headers={
                "HX-Redirect": "/categories",
            },
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
    except DatabaseAlreadyExistsExceptions:
        raise HTTPBadRequest(
            headers={
                "HX-Trigger": dumps(
                    {
                        "toast": ToastSchema(
                            message="Категория с таким названием уже существует"
                        ).model_dump()
                    }
                )
            },
        )


@router.put("/categories")
@require_login
async def categories_put(request: Request) -> Response:
    """
    (POST) Эндпоинт обновления категории
    :param request: Запрос от клиента
    :return: Response
    """

    db_session = await get_db_session()
    form = await request.post()

    try:
        data = CategorySchema.model_validate(form)
        category = await Category.find_by_id(db_session, data.id)

        if category is None:
            raise HTTPNotFound(
                headers={
                    "HX-Trigger": dumps(
                        {
                            "toast": ToastSchema(
                                message=f"Категория {data.id} не найдена"
                            ).model_dump()
                        }
                    )
                },
            )

        await category.update(db_session, name=data.name)

        return Response(
            status=200,
            text="Категория обновлена",
            headers={
                "HX-Refresh": "true",
            },
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
    except DatabaseAlreadyExistsExceptions:
        raise HTTPBadRequest(
            headers={
                "HX-Trigger": dumps(
                    {
                        "toast": ToastSchema(
                            message="Категория с таким названием уже существует"
                        ).model_dump()
                    }
                )
            },
        )


@router.delete("/categories")
@require_login
async def categories_delete(request: Request) -> Response:
    """
    (POST) Эндпоинт удаления категории
    :param request: Запрос от клиента
    :return: Response
    """

    db_session = await get_db_session()
    form = await request.post()

    try:
        data = CategorySchema.model_validate(form)
        category = await Category.find_by_id(db_session, data.id)

        if category is None:
            raise HTTPNotFound(
                headers={
                    "HX-Trigger": dumps(
                        {
                            "toast": ToastSchema(
                                message=f"Категория {data.id} не найдена"
                            ).model_dump()
                        }
                    )
                },
            )

        await category.delete(db_session)

        return Response(
            status=200,
            text="Категория удалена",
            headers={
                "HX-Refresh": "true",
            },
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


# endregion


# region ROUTES: /new_category


@router.get("/new_category")
@require_login
@template("new_category.jinja2")
async def new_category_view(_) -> dict:
    """
    (GET) Страница создания категории
    :return: dict
    """

    return {}


# endregion


# region ROUTES: /products


@router.get("/products")
@require_login
@template("products.jinja2")
async def products_view(_) -> dict[str, list[CategorySchema]]:
    """
    (GET) Страница товаров
    :return: dict[str, list[CategorySchema]]
    """

    db_session = await get_db_session()
    categories = await Category.get_all_categories(db_session)

    return {"products": categories}


# endregion
