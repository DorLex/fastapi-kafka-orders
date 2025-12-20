from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.accounts.models import UserModel
from src.accounts.services.auth import authenticate_user, create_access_token
from src.accounts.schemas.token import TokenSchema
from src.accounts.services.user import UserService
from src.__dependencies import get_session

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/token/', response_model=TokenSchema)
async def login_by_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
):
    """Авторизация"""

    db_user: UserModel = await UserService(session).get_by_username(form_data.username)

    auth_user: UserModel = authenticate_user(db_user, form_data.password)

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    access_token = create_access_token(auth_user)

    return TokenSchema(access_token=access_token)
