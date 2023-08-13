from typing import Optional, Self

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base
from src.schemas.user import UserSchema


class User(Base):
    user_id: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    username: Mapped[Optional[str]]

    @classmethod
    async def get_all_users(cls, db_session: AsyncSession) -> list[UserSchema]:
        """
        Получить всех зарегистрированных пользователей.
        :param db_session: Сессия базы данных
        :return: list[UserSchema]
        """

        stmt = select(cls)
        result = await db_session.execute(stmt)

        users = result.scalars().all()

        await db_session.close()

        return [
            UserSchema.model_validate(u, strict=False, from_attributes=True)
            for u in users
        ]

    @classmethod
    async def find_by_user_id(
        cls, db_session: AsyncSession, user_id: str
    ) -> Self | None:
        """
        Поиск пользователя с заданным User ID.
        :param db_session: Сессия базы данных
        :param user_id: User ID пользователя телеграма
        :return: User | None
        """

        stmt = select(cls).where(cls.user_id == user_id)
        result = await db_session.execute(stmt)

        await db_session.close()

        return result.scalars().first()
