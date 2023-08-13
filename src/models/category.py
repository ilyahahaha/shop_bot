from typing import Self, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base
from src.schemas.category import CategorySchema


class Category(Base):
    name: Mapped[str] = mapped_column(unique=True)

    products: Mapped[List["Product"]] = relationship(back_populates="category")  # noqa

    @classmethod
    async def get_all_categories(cls, db_session: AsyncSession) -> list[CategorySchema]:
        """
        Получить все категории пользователей.
        :param db_session: Сессия базы данных
        :return: list[CategorySchema]
        """

        stmt = select(cls)
        result = await db_session.execute(stmt)

        categories = result.scalars().all()

        await db_session.close()

        return [
            CategorySchema.model_validate(c, strict=False, from_attributes=True)
            for c in categories
        ]

    @classmethod
    async def find_by_name(cls, db_session: AsyncSession, name: str) -> Self | None:
        """
        Поиск категории по названию.
        :param db_session: Сессия базы данных
        :param name: Название категории
        :return: Category | None
        """

        stmt = select(cls).where(cls.name == name)
        result = await db_session.execute(stmt)

        await db_session.close()

        return result.scalars().first()
