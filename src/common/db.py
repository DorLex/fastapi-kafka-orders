from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.common.settings import config

async_engine: AsyncEngine = create_async_engine(
    config.postgresql_url,
    echo=config.sqlalchemy_echo,
)

AsyncSessionMaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    async_engine,
    expire_on_commit=False,  # влияет на возврат объекта при создании в БД с использованием session.flush()
)


# TODO: раскидать по разным файлам?
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionMaker() as session:
        yield session


class Base(DeclarativeBase):
    pass
