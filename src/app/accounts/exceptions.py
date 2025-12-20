from fastapi import HTTPException
from starlette import status

InvalidTokenException: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Неверный Токен',
)

CredentialsException: HTTPException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Не удалось проверить учетные данные',
)
