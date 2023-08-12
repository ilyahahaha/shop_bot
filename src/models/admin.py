from typing import Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.common.settings import Settings
from src.models.base import Base

settings = Settings()


class Admin(Base):
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    @classmethod
    async def find_by_username(
        cls, db_session: AsyncSession, username: str
    ) -> Self | None:
        """
        Поиск администратора с заданным именем.
        :param db_session: Сессия базы данных
        :param username: Имя пользователя
        :return: Admin | None
        """

        stmt = select(cls).where(cls.username == username)
        result = await db_session.execute(stmt)

        return result.scalars().first()
