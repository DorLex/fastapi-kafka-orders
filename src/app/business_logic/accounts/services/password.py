from logging import Logger, getLogger

from argon2 import PasswordHasher

logger: Logger = getLogger(__name__)

password_hasher: PasswordHasher = PasswordHasher()


class PasswordService:
    @staticmethod
    def generate_password_hash(raw_password: str) -> str:
        hashed_password: str = password_hasher.hash(raw_password)
        return hashed_password

    @staticmethod
    def verify_password(raw_password: str, hashed_password: str) -> bool:
        try:
            is_password_valid: bool = password_hasher.verify(hashed_password, raw_password)
            return is_password_valid
        except Exception as exc:
            logger.warning(f'Ошибка при валидации пароля: "{exc}"')

        return False
