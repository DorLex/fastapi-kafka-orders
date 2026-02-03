from fastapi import APIRouter, Body, Depends
from fastapi.security import HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.business_logic.accounts.dto.token import TokenResponseDTO
from src.app.business_logic.accounts.services.jwt import JWTService
from src.app.infrastructure.accounts.repositories.user import UserRepository
from src.common.db.dependencies import get_db

router: APIRouter = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)


@router.post('/token')
async def login(
    credentials: HTTPBasicCredentials = Body(examples=[{'username': 'user_1', 'password': '123456789'}]),
    db: AsyncSession = Depends(get_db),
) -> TokenResponseDTO:
    """Авторизация."""
    jwt_service: JWTService = JWTService(UserRepository(db))
    return await jwt_service.generate_jwt(credentials)
