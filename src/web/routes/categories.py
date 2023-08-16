from json import dumps

from aiohttp.web import RouteTableDef, Request, Response
from aiohttp.web_exceptions import HTTPBadRequest, HTTPNotFound
from aiohttp_jinja2 import template
from pydantic import ValidationError

from src.common.database import get_session as get_db_session
from src.common.exceptions import DatabaseAlreadyExistsExceptions
from src.models import Category
from src.schemas.category import CategorySchema, EditCategorySchema
from src.schemas.toast import ToastSchema
from src.utils.web.require_login import require_login

router = RouteTableDef()


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


@router.get("/new_category")
@require_login
@template("new_category.jinja2")
async def new_category_view(_) -> dict:
    """
    (GET) Страница создания категории
    :return: dict
    """

    return {}
