from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.bll.accounts.dependencies.user import get_current_user
from src.app.bll.accounts.dto.token import TokenPayloadDTO
from src.app.bll.accounts.dto.user import UserCreateDTO, UserResponseDTO
from src.app.bll.accounts.dto.user_with_orders import UserWithOrdersDTO
from src.app.bll.accounts.services.jwt import JWTService
from src.app.bll.accounts.services.user import UserService
from src.app.dal.accounts.models.user import User
from src.app.dal.accounts.repositories.user import UserRepository
from src.common.db.dependencies import get_db

router: APIRouter = APIRouter(
    prefix='/users',
    tags=['Users'],
    # dependencies=[Depends(AuthService.verify_token)], # TODO: подумать, как лучше переключать auth
)


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseDTO,
)
async def registration(user_data: UserCreateDTO, db: AsyncSession = Depends(get_db)) -> User:
    """Регистрация пользователя."""

    user_service: UserService = UserService(UserRepository(db))
    user: User = await user_service.create_user(user_data)
    await db.commit()

    return user


@router.get(
    '',
    response_model=list[UserResponseDTO],
)
async def get_users(
    skip: int = 0,
    limit: int = 100,
    _token_data: TokenPayloadDTO = Depends(JWTService.decode_token),
    db: AsyncSession = Depends(get_db),
) -> list[User]:
    """Получить список пользователей."""
    user_service: UserService = UserService(UserRepository(db))
    users: list[User] = await user_service.get_users(skip, limit)
    return users


@router.get('/me')
async def get_user_me(current_user: UserResponseDTO = Depends(get_current_user)) -> UserResponseDTO:
    """Получить текущего пользователя."""
    return current_user


@router.get('/with-orders', response_model=list[UserWithOrdersDTO])
async def get_users_with_orders(
    skip: int = 0,
    limit: int = 100,
    _token_data: TokenPayloadDTO = Depends(JWTService.decode_token),
    db: AsyncSession = Depends(get_db),
):
    """Получить пользователей с заказами."""

    user_service: UserService = UserService(UserRepository(db))
    users_with_orders: list[User] = await user_service.get_users_with_orders(skip, limit)
    return users_with_orders
