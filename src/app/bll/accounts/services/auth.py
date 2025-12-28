from datetime import datetime, timedelta, timezone
from logging import getLogger, Logger
from typing import Any

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.bll.accounts.dto.token import TokenPayloadDTO, TokenResponseDTO
from src.app.bll.accounts.exceptions.auth import (
    FailedCredentialsException,
    InvalidCredentialsException,
    InvalidTokenException,
)
from src.app.bll.accounts.services.password import PasswordService
from src.app.bll.accounts.services.user import UserService
from src.app.dal.accounts.models.user import User
from src.app.dal.accounts.repositories.user import UserRepository
from src.common.constants.auth import JWT_ALGORITHM
from src.common.db.objs import get_db
from src.common.envs import env_config

logger: Logger = getLogger(__name__)

# TODO: в какой файл|куда положить этот объект?
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='/auth/token/')


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def _generate_token_expire(self) -> datetime:
        token_expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=env_config.jwt_expiration_minutes)
        return token_expire

    async def generate_jwt(self, form_data: OAuth2PasswordRequestForm) -> TokenResponseDTO:
        user: User = await self.repository.get_user_by_username(form_data.username)

        if not PasswordService.verify_password(form_data.password, user.hashed_password):
            raise InvalidCredentialsException

        token_expire: datetime = self._generate_token_expire()

        payload: dict = {'user_id': user.id, 'username': user.username, 'exp': token_expire}
        encoded_jwt: str = jwt.encode(payload, env_config.jwt_secret_key, algorithm=JWT_ALGORITHM)

        return TokenResponseDTO(access_token=encoded_jwt)

    @staticmethod
    def verify_token(token: str = Depends(oauth2_scheme)) -> TokenPayloadDTO:
        try:
            payload: dict[str, Any] = jwt.decode(token, env_config.jwt_secret_key, algorithms=[JWT_ALGORITHM])

            user_id: int = payload.get('user_id')
            username: str = payload.get('username')

            if not user_id or not username:
                raise InvalidTokenException

            return TokenPayloadDTO(user_id=user_id, username=username)

        except JWTError as exc:
            logger.warning(exc)
            raise InvalidTokenException


async def get_current_user(
    token_data: TokenPayloadDTO = Depends(AuthService.verify_token),
    db: AsyncSession = Depends(get_db),
) -> User:
    user_service: UserService = UserService(UserRepository(db))
    user: User = await user_service.get_user_by_id(token_data.user_id)
    if not user:
        raise FailedCredentialsException

    return user  # TODO: лучше возвращать UserDTO, а не БД-сущность
