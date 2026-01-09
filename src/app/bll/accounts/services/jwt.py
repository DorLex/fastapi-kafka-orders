from datetime import UTC, datetime, timedelta
from logging import Logger, getLogger
from typing import TYPE_CHECKING, Any

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBasicCredentials
from jose import JWTError, jwt

from src.app.bll.accounts.dependencies.auth import http_bearer
from src.app.bll.accounts.dto.token import TokenPayloadDTO, TokenResponseDTO
from src.app.bll.accounts.exceptions.auth import (
    FailedCredentialsException,
    InvalidCredentialsException,
    InvalidTokenException,
)
from src.app.bll.accounts.services.password import PasswordService
from src.app.dal.accounts.repositories.user import UserRepository
from src.common.constants.auth import JWT_ALGORITHM
from src.common.envs import env_config

if TYPE_CHECKING:
    from src.app.bll.accounts.dto.user import UserHashedPasswordDTO

logger: Logger = getLogger(__name__)


class JWTService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def _generate_token_expire(self) -> datetime:
        token_expire: datetime = datetime.now(UTC) + timedelta(minutes=env_config.jwt_expiration_minutes)
        return token_expire

    async def generate_jwt(self, credentials: HTTPBasicCredentials) -> TokenResponseDTO:
        user: UserHashedPasswordDTO | None = await self.repository.get_user_for_login(credentials.username)
        if not user:
            raise InvalidCredentialsException

        if not PasswordService.verify_password(credentials.password, user.hashed_password):
            raise InvalidCredentialsException

        token_expire: datetime = self._generate_token_expire()

        payload: dict = {'user_id': user.id, 'username': user.username, 'exp': token_expire}
        encoded_jwt: str = jwt.encode(payload, env_config.jwt_secret_key, algorithm=JWT_ALGORITHM)

        return TokenResponseDTO(access_token=encoded_jwt)

    @staticmethod
    def decode_token(token: HTTPAuthorizationCredentials = Depends(http_bearer)) -> TokenPayloadDTO:
        try:
            payload: dict[str, Any] = jwt.decode(
                token.credentials,
                env_config.jwt_secret_key,
                algorithms=[JWT_ALGORITHM],
            )

            return TokenPayloadDTO(
                user_id=payload.get('user_id'),
                username=payload.get('username'),
            )

        except JWTError as exc:
            logger.warning(exc)
            raise InvalidTokenException from None

        except Exception as exc:
            logger.error(exc)
            raise FailedCredentialsException from None
