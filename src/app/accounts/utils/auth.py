from datetime import datetime, timezone, timedelta

from src.app.accounts.config import pwd_context


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_token_expire(expire):
    token_expire = datetime.now(timezone.utc) + timedelta(minutes=expire)
    return token_expire
