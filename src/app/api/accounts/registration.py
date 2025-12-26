from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.dal.accounts.models.user import User
from src.app.bll.accounts.dto.user import UserCreateSchema, UserResponseDTO
from src.app.bll.accounts.services.user import UserService
from src.common.db import get_db

router: APIRouter = APIRouter(
    prefix='/registration',
    tags=['Registration'],
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponseDTO,
)
async def user_registration(user_data: UserCreateSchema, db: AsyncSession = Depends(get_db)) -> User:
    """Регистрация пользователя"""

    user: User = await UserService(db).registration(user_data)
    await db.commit()

    return user
