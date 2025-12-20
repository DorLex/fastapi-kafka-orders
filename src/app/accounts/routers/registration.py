from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.accounts.models import User
from src.app.accounts.schemas.user import UserCreateSchema, UserOutSchema
from src.app.accounts.services.user import UserService
from src.__dependencies import get_session

router = APIRouter(
    prefix='/registration',
    tags=['registration'],
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
async def user_registration(user: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    """Регистрация пользователя"""

    db_user: User = await UserService(session).registration(user)
    await session.commit()

    return db_user
