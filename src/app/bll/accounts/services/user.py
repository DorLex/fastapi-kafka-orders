from fastapi import HTTPException
from starlette import status

from src.app.bll.accounts.dto.user import UserCreateDTO, UserResponseDTO
from src.app.dal.accounts.models.user import User
from src.app.dal.accounts.repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create_user(self, user_data: UserCreateDTO) -> UserResponseDTO:
        user_exists: bool = await self.repository.check_user_exists(
            username=user_data.username,
            email=user_data.email,
        )

        if user_exists:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Пользователь с таким именем или почтой уже зарегистрирован',
            )

        return await self.repository.create(user_data)

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[UserResponseDTO]:
        return await self.repository.get_users(skip, limit)

    async def get_users_with_orders(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.repository.get_users_with_orders(skip, limit)

    async def get_users_filter_by(self, **filters) -> list[User]:
        return await self.repository.get_users_filter_by(**filters)

    async def get_user_by_id(self, user_id: int) -> UserResponseDTO | None:
        return await self.repository.get_user_by_id(user_id)
