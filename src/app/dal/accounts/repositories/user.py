from sqlalchemy import ScalarResult, select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.bll.accounts.dto.user import UserCreateDTO
from src.app.bll.accounts.services.password import PasswordService
from src.app.dal.accounts.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    # TODO: в репо возвращать DTO, а не модели

    async def create(self, user_data: UserCreateDTO) -> User:
        hashed_password: str = PasswordService.generate_password_hash(user_data.password)

        user: User = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        await self.db.flush()

        return user

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        query: Select = select(User).offset(skip).limit(limit)
        result: ScalarResult[User] = await self.db.scalars(query)
        return result.all()

    async def get_users_with_orders(self, skip: int = 0, limit: int = 100) -> list[User]:
        query: Select = (
            select(User)
            .options(joinedload(User.orders))
            .order_by(User.id)
            .offset(skip)
            .limit(limit)
        )

        result: ScalarResult[User] = await self.db.scalars(query)
        return result.unique().all()

    async def get_users_filter_by(self, **filters) -> list[User]:
        query: Select = select(User).filter_by(**filters)
        result: ScalarResult[User] = await self.db.scalars(query)
        return result.all()

    async def get_user_by_username(self, username: str) -> User:
        query: Select = select(User).where(User.username == username)
        return await self.db.scalar(query)

    async def get_user_by_id(self, user_id: int) -> User:
        query: Select = select(User).where(User.id == user_id)
        return await self.db.scalar(query)
