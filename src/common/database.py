from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from src.common.settings import Settings

settings = Settings()

engine = create_async_engine(
    settings.postgres_url.unicode_string(),
    future=True,
    echo=True,
)

create_async_session = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_session() -> AsyncSession:
    async with create_async_session() as session:
        return session

