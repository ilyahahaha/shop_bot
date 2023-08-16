from typing import Optional

from sqlalchemy import ForeignKey, String, ARRAY, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base
from src.schemas.product import ProductSchema


class Product(Base):
    category_id: Mapped[str] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(
        back_populates="products", lazy="subquery"
    )  # noqa
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    images_url: Mapped[list[str]] = mapped_column(ARRAY(String))

    @classmethod
    async def get_all_products(cls, db_session: AsyncSession) -> list[ProductSchema]:
        """
        Получить все товары.
        :param db_session: Сессия базы данных
        :return: list[CategorySchema]
        """

        stmt = select(cls)
        result = await db_session.execute(stmt)

        categories = result.scalars().all()

        await db_session.close()

        return [
            ProductSchema.model_validate(c, strict=False, from_attributes=True)
            for c in categories
        ]
