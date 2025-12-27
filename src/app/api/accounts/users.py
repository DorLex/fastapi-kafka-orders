from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.bll.accounts.dto.user import UserResponseDTO
from src.app.bll.accounts.dto.user_with_orders import UserWithOrdersDTO
from src.app.bll.accounts.services.auth import AuthService, get_current_user
from src.app.bll.accounts.services.user import UserService
from src.app.dal.accounts.models.user import User
from src.app.dal.accounts.repositories.user import UserRepository
from src.common.db import get_db

router: APIRouter = APIRouter(
    prefix='/users',
    tags=['Users'],
    dependencies=[Depends(AuthService.verify_token)],
)


@router.get(
    '',
    response_model=list[UserResponseDTO],
)
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)) -> list[User]:
    """Получить список пользователей."""
    user_service: UserService = UserService(UserRepository(db))
    users: list[User] = await user_service.get_users(skip, limit)
    return users


@router.get(
    '/me',
    response_model=UserResponseDTO,
)
async def get_user_me(current_user: User = Depends(get_current_user)):
    """Получить текущего пользователя."""
    return current_user


@router.get('/with-orders/', response_model=list[UserWithOrdersDTO])
async def read_users_with_orders(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Показать пользователей с заказами"""

    users_with_orders: list[User] = await UserService(db).get_users_with_orders(skip, limit)
    return users_with_orders
