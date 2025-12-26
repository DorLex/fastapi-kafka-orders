from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.app.dal.accounts.models.user import User
from src.app.dal.accounts.repositories.user import UserRepository
from src.app.bll.accounts.dto.token import TokenResponseDTO
from src.app.bll.accounts.services.auth import check_credentials, create_access_token
from src.app.bll.accounts.services.user import UserService
from src.common.db import get_db

router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post('/token/', response_model=TokenResponseDTO)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: AsyncSession = Depends(get_db),
) -> TokenResponseDTO:
    """Авторизация."""

    user_service: UserService = UserService(UserRepository(db))
    user: User = await user_service.get_user_by_username(form_data.username)

    # TODO: убрать это в UserService или в AuthService
    valid_credentials: bool = check_credentials(user, form_data.password)
    if not valid_credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверное имя пользователя или пароль',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return TokenResponseDTO(access_token=create_access_token(user))
