import os

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

MODE = os.getenv('MODE')

DB_USER_TEST = os.getenv('POSTGRES_USER')
DB_PASS_TEST = os.getenv('POSTGRES_PASSWORD')
DB_HOST_TEST = os.getenv('POSTGRES_HOST')
DB_PORT_TEST = os.getenv('POSTGRES_PORT')
DB_NAME_TEST = os.getenv('POSTGRES_DB')

DATABASE_URL_TEST = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

async_engine_test = create_async_engine(
    DATABASE_URL_TEST,
    poolclass=NullPool,
    # echo=True
)

SessionTest = async_sessionmaker(
    async_engine_test,
    expire_on_commit=False
)
