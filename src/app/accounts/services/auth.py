from datetime import datetime
from logging import Logger, getLogger
from typing import Any

from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.accounts.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from src.app.accounts.dependencies import oauth2_scheme
from src.app.accounts.dto.token import TokenDTO
from src.app.accounts.exceptions import CredentialsException, InvalidTokenException
from src.app.accounts.models import User
from src.app.accounts.repositories.user import UserRepository
from src.app.accounts.services.user import UserService
from src.app.accounts.utils.auth import generate_token_expire, verify_password
from src.common.db import get_db

logger: Logger = getLogger(__name__)


# TODO: создать AuthService

def create_access_token(user: User) -> str:
    token_expire: datetime = generate_token_expire(ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict = {'user_id': user.id, 'username': user.username, 'exp': token_expire}
    encoded_jwt: str = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def check_credentials(user: User, password: str) -> bool:
    if not verify_password(password, user.hashed_password):
        return False
    return True


def verify_token(token: str = Depends(oauth2_scheme)) -> TokenDTO:
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: int = payload.get('user_id')
        username: str = payload.get('username')

        if not user_id or not username:
            raise InvalidTokenException

        return TokenDTO(user_id=user_id, username=username)

    except JWTError as exc:
        logger.warning(exc)
        raise InvalidTokenException


async def get_current_user(
    token_data: TokenDTO = Depends(verify_token),
    db: AsyncSession = Depends(get_db),
) -> User:
    user_service: UserService = UserService(UserRepository(db))
    user: User = await user_service.get_user_by_id(token_data.user_id)
    if not user:
        raise CredentialsException

    # TODO: лучше возвращать UserDTO, а не БД-сущность
    return user
