from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.accounts.models import UserModel
from src.accounts.schemas.user import UserCreateSchema, UserOutSchema
from src.accounts.services.user import UserService
from src.__dependencies import get_session

router = APIRouter(
    prefix='/registration',
    tags=['registration'],
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
async def user_registration(user: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    """Регистрация пользователя"""

    db_user: UserModel = await UserService(session).registration(user)
    await session.commit()

    return db_user
