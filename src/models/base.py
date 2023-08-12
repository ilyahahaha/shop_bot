from cuid2 import Cuid
from sqlalchemy import String
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    declared_attr,
    mapped_column,
    Mapped,
    DeclarativeBase,
)

from src.common.exceptions import DatabaseAlreadyExistsExceptions, DatabaseUnknownError

cuid = Cuid(length=16)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(String(16), primary_key=True, default=cuid.generate)
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return self.__name__.lower()

    async def save(self, db_session: AsyncSession) -> None:
        """
        Сохранить модель в базу данных.
        :param db_session: Сессия базы данных
        :return: None
        """

        try:
            db_session.add(self)

            return await db_session.commit()
        except IntegrityError:
            raise DatabaseAlreadyExistsExceptions(
                "Модель с указанными данными уже существует"
            )
        except SQLAlchemyError:
            raise DatabaseUnknownError("Не удалось создать модель")

    async def delete(self, db_session: AsyncSession) -> None:
        """
        Сохранить изменения в модели.
        :param db_session: Сессия базы данных
        :return: None
        """

        try:
            await db_session.delete(self)

            return await db_session.commit()
        except SQLAlchemyError:
            raise DatabaseUnknownError("Не удалось удалить модель")

    async def update(self, db_session: AsyncSession, **kwargs) -> None:
        """
        Обновить модель в базе данных.
        :param db_session: Сессия базы данных
        :param kwargs: Поля модели для обновления
        :return: None
        """

        try:
            for k, v in kwargs.items():
                setattr(self, k, v)

            return await db_session.commit()
        except SQLAlchemyError:
            raise DatabaseUnknownError("Не удалось обновить модель")
