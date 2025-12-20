import os

from passlib.context import CryptContext

SECRET_KEY = os.getenv('SECRET_KEY')

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
