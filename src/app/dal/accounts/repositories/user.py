from pydantic import EmailStr
from sqlalchemy import or_, ScalarResult, select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.app.bll.accounts.dto.user import UserCreateDTO, UserHashedPasswordDTO, UserResponseDTO
from src.app.bll.accounts.dto.user_with_orders import UserWithOrdersDTO
from src.app.bll.accounts.services.password import PasswordService
from src.app.bll.common.dto.filter import PaginationParams
from src.app.dal.accounts.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, user_data: UserCreateDTO) -> UserResponseDTO:
        hashed_password: str = PasswordService.generate_password_hash(user_data.password)

        user: User = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        self.db.add(user)
        await self.db.flush()

        return UserResponseDTO.model_validate(user)

    async def get_users(self, filters: PaginationParams) -> list[UserResponseDTO]:
        query: Select = select(User).limit(filters.limit).offset(filters.offset)
        result: ScalarResult[User] = await self.db.scalars(query)

        return [UserResponseDTO.model_validate(user) for user in result.all()]

    async def get_user_by_id(self, user_id: int) -> UserResponseDTO | None:
        query: Select = select(User).where(User.id == user_id)
        user: User | None = await self.db.scalar(query)

        return UserResponseDTO.model_validate(user) if user else None

    async def get_user_for_login(self, username: str) -> UserHashedPasswordDTO | None:
        query: Select = select(User).where(User.username == username)
        user: User | None = await self.db.scalar(query)

        return UserHashedPasswordDTO.model_validate(user) if user else None

    async def check_user_exists(self, username: str, email: EmailStr | str) -> bool:
        query: Select = select(
            select(1)
            .select_from(User)
            .where(
                or_(
                    User.username == username,
                    User.email == email,
                ),
            )
            .limit(1)
            .exists(),
        )

        return await self.db.scalar(query)

    async def get_users_with_orders(self, filters: PaginationParams) -> list[UserWithOrdersDTO]:
        query: Select = (
            select(User)
            .options(joinedload(User.orders))
            .order_by(User.id)
            .limit(filters.limit)
            .offset(filters.offset)
        )

        result: ScalarResult[User] = await self.db.scalars(query)
        return [UserWithOrdersDTO.model_validate(user) for user in result.unique().all()]
