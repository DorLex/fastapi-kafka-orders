import os

from dotenv import load_dotenv
from passlib.context import CryptContext

from src.config import DOTENV_PATH

load_dotenv(DOTENV_PATH)

SECRET_KEY = os.getenv('SECRET_KEY')

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
