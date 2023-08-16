from aiohttp.web import RouteTableDef
from aiohttp_jinja2 import template

from src.common.database import get_session as get_db_session
from src.models import Product, Category
from src.schemas.category import CategorySchema
from src.schemas.product import ProductSchema
from src.utils.web.require_login import require_login

router = RouteTableDef()


@router.get("/products")
@require_login
@template("products.jinja2")
async def products_view(_) -> dict[str, list[ProductSchema]]:
    """
    (GET) Страница товаров
    :return: dict[str, list[ProductSchema]]
    """

    db_session = await get_db_session()

    products = await Product.get_all_products(db_session)
    categories = await Category.get_all_categories(db_session)

    return {"products": products, "categories": categories}


@router.get("/new_product")
@require_login
@template("new_product.jinja2")
async def new_product_view(_) -> dict[str, list[CategorySchema]]:
    """
    (GET) Страница создания товара
    :return: dict
    """

    db_session = await get_db_session()
    categories = await Category.get_all_categories(db_session)

    return {"categories": categories}
