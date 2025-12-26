import os

from passlib.context import CryptContext

# TODO: убрать в норм конфиг
SECRET_KEY = os.getenv('SECRET_KEY')

ALGORITHM: str = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
