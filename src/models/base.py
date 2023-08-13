from typing import Self

from cuid2 import Cuid
from sqlalchemy import String, select
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

            await db_session.commit()
        except IntegrityError:
            raise DatabaseAlreadyExistsExceptions(
                "Модель с указанными данными уже существует"
            )
        except SQLAlchemyError:
            raise DatabaseUnknownError("Не удалось создать модель")
        finally:
            await db_session.close()

    async def delete(self, db_session: AsyncSession) -> None:
        """
        Сохранить изменения в модели.
        :param db_session: Сессия базы данных
        :return: None
        """

        try:
            await db_session.delete(self)

            await db_session.commit()
        except SQLAlchemyError:
            raise DatabaseUnknownError("Не удалось удалить модель")
        finally:
            await db_session.close()

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

            db_session.add(self)
            await db_session.commit()
        except SQLAlchemyError:
            raise DatabaseUnknownError("Не удалось обновить модель")
        finally:
            await db_session.close()

    @classmethod
    async def find_by_id(cls, db_session: AsyncSession, id: str) -> Self:
        """
        Поиск модели по ID.
        :param db_session: Сессия базы данных
        :param id: ID модели
        :return: self
        """

        stmt = select(cls).where(cls.id == id)
        result = await db_session.execute(stmt)

        await db_session.close()

        return result.scalars().first()
