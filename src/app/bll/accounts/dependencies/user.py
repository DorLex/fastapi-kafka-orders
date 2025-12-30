from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.bll.accounts.dto.token import TokenPayloadDTO
from src.app.bll.accounts.dto.user import UserResponseDTO
from src.app.bll.accounts.exceptions.auth import FailedCredentialsException
from src.app.bll.accounts.services.jwt import JWTService
from src.app.bll.accounts.services.user import UserService
from src.app.dal.accounts.repositories.user import UserRepository
from src.common.db.dependencies import get_db


async def get_current_user(
    token_data: TokenPayloadDTO = Depends(JWTService.decode_token),
    db: AsyncSession = Depends(get_db),
) -> UserResponseDTO:
    user_service: UserService = UserService(UserRepository(db))
    user: UserResponseDTO | None = await user_service.get_user_by_id(token_data.user_id)
    if not user:
        raise FailedCredentialsException

    return user
