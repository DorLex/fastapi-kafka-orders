from fastapi import HTTPException
from starlette import status

from src.app.business_logic.accounts.dto.user import UserCreateDTO, UserResponseDTO
from src.app.business_logic.accounts.dto.user_with_orders import UserWithOrdersDTO
from src.app.business_logic.common.dto.filters import PaginationParams
from src.app.infrastructure.accounts.repositories.user import UserRepository


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

    async def get_users(self, filters: PaginationParams) -> list[UserResponseDTO]:
        return await self.repository.get_users(filters)

    async def get_user_by_id(self, user_id: int) -> UserResponseDTO | None:
        return await self.repository.get_user_by_id(user_id)

    async def get_users_with_orders(self, filters: PaginationParams) -> list[UserWithOrdersDTO]:
        return await self.repository.get_users_with_orders(filters)
