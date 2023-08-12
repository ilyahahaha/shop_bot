from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

from src.common.settings import Settings
from src.utils.singleton import singleton

settings = Settings()

engine = create_async_engine(
    settings.asyncpg_url.unicode_string(),
    future=True,
    echo=True,
)

create_session = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


@singleton
class Database:
    def __init__(self):
        self.session = None

    async def get_session(self) -> AsyncSession:
        if self.session is None:
            async with create_session() as session:
                self.session = session

        return self.session
