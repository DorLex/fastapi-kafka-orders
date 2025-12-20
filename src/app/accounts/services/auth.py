from fastapi import Depends
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.accounts.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.app.accounts.exceptions import InvalidTokenException, CredentialsException
from src.app.accounts.models import User
from src.app.accounts.schemas.token import TokenDataSchema
from src.app.accounts.services.user import UserService
from src.app.accounts.utils.auth import verify_password, generate_token_expire
from src.app.accounts.dependencies import oauth2_scheme
from src.__dependencies import get_session


def create_access_token(user: User) -> str:
    token_expire = generate_token_expire(ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {'user_id': user.id, 'username': user.username, 'exp': token_expire}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def authenticate_user(db_user: User, password: str) -> User | bool:
    if not db_user:
        return False
    if not verify_password(password, db_user.hashed_password):
        return False
    return db_user


def verify_token(token: str = Depends(oauth2_scheme)) -> TokenDataSchema:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id: int = payload.get('user_id')
        username: str = payload.get('username')

        if not user_id or not username:
            raise InvalidTokenException

        token_data = TokenDataSchema(user_id=user_id, username=username)

    except JWTError:
        raise InvalidTokenException

    return token_data


async def get_current_user(
    token_data: TokenDataSchema = Depends(verify_token),
    session: AsyncSession = Depends(get_session),
) -> User:
    db_user: User = await UserService(session).get_by_id(token_data.user_id)
    if not db_user:
        raise CredentialsException
    return db_user
