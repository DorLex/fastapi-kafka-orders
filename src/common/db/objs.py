from collections.abc import AsyncGenerator
from datetime import datetime

from sqlalchemy import BIGINT, DateTime, func
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.common.envs import env_config

async_engine: AsyncEngine = create_async_engine(
    env_config.postgresql_url,
    echo=env_config.sqlalchemy_echo,
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
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
