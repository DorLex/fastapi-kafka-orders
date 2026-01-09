from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db.connection import AsyncSessionMaker


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionMaker() as session:
        yield session
