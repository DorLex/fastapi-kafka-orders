from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.accounts.models import User
from src.app.accounts.schemas import UserCreateSchema
from src.app.accounts.utils.auth import get_password_hash


class UserRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: UserCreateSchema) -> User:
        hashed_password = get_password_hash(user.password)

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
        )

        self._session.add(db_user)
        await self._session.flush()

        return db_user

    async def get_all(self, skip: int = 0, limit: int = 100):
        query = select(User).offset(skip).limit(limit)
        result = await self._session.scalars(query)
        return result.all()

    async def get_all_with_orders(self, skip: int = 0, limit: int = 100):
        query = (
            select(User)
            .options(joinedload(User.orders))
            .order_by(User.id)
            .offset(skip).limit(limit)
        )

        result = await self._session.scalars(query)
        return result.unique().all()

    async def get_filter_by(self, **filters):
        query = select(User).filter_by(**filters)
        result = await self._session.scalars(query)
        return result.all()

    async def get_by_username(self, username: str) -> User:
        query = select(User).where(User.username == username)
        return await self._session.scalar(query)

    async def get_by_id(self, user_id: int) -> User:
        query = select(User).where(User.id == user_id)
        return await self._session.scalar(query)
