from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.bll.accounts.dto.token import TokenResponseDTO
from src.app.bll.accounts.services.auth import AuthService
from src.app.dal.accounts.repositories.user import UserRepository
from src.common.db.objs import get_db

router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/token', response_model=TokenResponseDTO)
async def login(
    credentials: HTTPBasicCredentials,
    db: AsyncSession = Depends(get_db),
) -> TokenResponseDTO:
    """Авторизация."""

    auth_service: AuthService = AuthService(UserRepository(db))
    return await auth_service.generate_jwt(credentials)
