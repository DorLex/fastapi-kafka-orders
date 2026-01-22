from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.business_logic.accounts.dependencies.user import get_current_user
from src.app.business_logic.accounts.dto.user import UserCreateDTO, UserResponseDTO
from src.app.business_logic.accounts.dto.user_with_orders import UserWithOrdersDTO
from src.app.business_logic.accounts.services.user import UserService
from src.app.business_logic.common.dto.filters import PaginationParams
from src.app.infrastructure.accounts.repositories.user import UserRepository
from src.common.db.dependencies import get_db

router: APIRouter = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
)
async def registration(user_data: UserCreateDTO, db: AsyncSession = Depends(get_db)) -> UserResponseDTO:
    """Регистрация пользователя."""
    user_service: UserService = UserService(UserRepository(db))
    user: UserResponseDTO = await user_service.create_user(user_data)
    await db.commit()

    return user


@router.get('')
async def get_users(
    filters: PaginationParams = Query(),
    _current_user: UserResponseDTO = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[UserResponseDTO]:
    """Получить список пользователей."""
    user_service: UserService = UserService(UserRepository(db))
    users: list[UserResponseDTO] = await user_service.get_users(filters)
    return users


@router.get('/me')
async def get_user_me(current_user: UserResponseDTO = Depends(get_current_user)) -> UserResponseDTO:
    """Получить текущего пользователя."""
    return current_user


@router.get('/with-orders')
async def get_users_with_orders(
    filters: PaginationParams = Query(),
    _current_user: UserResponseDTO = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[UserWithOrdersDTO]:
    """Получить пользователей с заказами."""
    user_service: UserService = UserService(UserRepository(db))
    users_with_orders: list[UserWithOrdersDTO] = await user_service.get_users_with_orders(filters)
    return users_with_orders
