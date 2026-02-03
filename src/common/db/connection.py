from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from src.common.envs import env_config

async_engine: AsyncEngine = create_async_engine(
    env_config.postgresql_url,
    echo=env_config.sqlalchemy_echo,
)

AsyncSessionMaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    async_engine,
    expire_on_commit=False,  # влияет на возврат объекта при создании в БД с использованием session.flush()
)
