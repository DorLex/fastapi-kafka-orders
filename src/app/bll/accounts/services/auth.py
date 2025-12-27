from datetime import datetime, timedelta, timezone
from logging import getLogger, Logger
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app._accounts.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from src.app._accounts.dependencies import oauth2_scheme
from src.app.bll.accounts.dto.token import TokenDTO, TokenResponseDTO
from src.app.bll.accounts.exceptions.auth import (
    FailedCredentialsException,
    InvalidCredentialsException,
    InvalidTokenException,
)
from src.app.bll.accounts.services.user import UserService
from src.app.bll.accounts.utils.auth import PasswordService
from src.app.dal.accounts.models.user import User
from src.app.dal.accounts.repositories.user import UserRepository
from src.common.db import get_db

logger: Logger = getLogger(__name__)


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def _generate_token_expire(self, expire: int) -> datetime:
        token_expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=expire)
        return token_expire

    async def generate_jwt(self, form_data: OAuth2PasswordRequestForm) -> TokenResponseDTO:
        user: User = await self.repository.get_user_by_username(form_data.username)

        if not PasswordService.verify_password(form_data.password, user.hashed_password):
            raise InvalidCredentialsException

        token_expire: datetime = self._generate_token_expire(ACCESS_TOKEN_EXPIRE_MINUTES)

        payload: dict = {'user_id': user.id, 'username': user.username, 'exp': token_expire}
        encoded_jwt: str = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return TokenResponseDTO(access_token=encoded_jwt)

    @staticmethod
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
    token_data: TokenDTO = Depends(AuthService.verify_token),
    db: AsyncSession = Depends(get_db),
) -> User:
    user_service: UserService = UserService(UserRepository(db))
    user: User = await user_service.get_user_by_id(token_data.user_id)
    if not user:
        raise FailedCredentialsException

    return user  # TODO: лучше возвращать UserDTO, а не БД-сущность
