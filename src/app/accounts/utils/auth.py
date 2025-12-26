from datetime import datetime, timezone, timedelta

from src.app.accounts.config import pwd_context


def get_password_hash(password: str) -> str:
    hashed_password: str = pwd_context.hash(password)
    print()
    print(f'{type(hashed_password)=}')
    print()
    return hashed_password


def verify_password(raw_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(raw_password, hashed_password)


def generate_token_expire(expire: int) -> datetime:
    token_expire: datetime = datetime.now(timezone.utc) + timedelta(minutes=expire)
    return token_expire
