from fastapi import HTTPException
from starlette import status

from src.app.bll.accounts.dto.user import UserCreateSchema
from src.app.dal.accounts.models.user import User
from src.app.dal.accounts.repositories.user import UserRepository


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def create_user(self, user_data: UserCreateSchema):
        check_user_registered = await self.get_users_filter_by(username=user_data.username, email=user_data.email)
        if check_user_registered:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                'Пользователь с таким именем и почтой уже зарегистрирован',
            )

        return await self.repository.create(user_data)

    async def get_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.repository.get_users(skip, limit)

    async def get_users_with_orders(self, skip: int = 0, limit: int = 100) -> list[User]:
        return await self.repository.get_users_with_orders(skip, limit)

    async def get_users_filter_by(self, **filters) -> list[User]:
        return await self.repository.get_users_filter_by(**filters)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.repository.get_user_by_id(user_id)
